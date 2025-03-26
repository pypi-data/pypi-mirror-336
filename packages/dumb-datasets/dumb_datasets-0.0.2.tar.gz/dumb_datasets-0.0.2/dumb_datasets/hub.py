"""Hub integration module for interfacing with the HuggingFace Hub.

provides functions for authenticating with and downloading from the huggingface hub.
"""

import datetime
import hashlib
import json
import os
import uuid
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Any, Callable, Dict, Generator, Iterable, Optional, Union, cast

from huggingface_hub import (  # type: ignore[import-untyped]
    HfApi,
    create_branch,  # type: ignore[import-untyped]
    hf_hub_download,
    snapshot_download,
)
from huggingface_hub.hf_api import DatasetInfo, ModelInfo  # type: ignore[import-untyped]
from loguru import logger  # type: ignore[import-not-found]
from tenacity import retry, stop_after_attempt, wait_exponential  # type: ignore[import-not-found]

from dumb_datasets.config import get_config
from dumb_datasets.exceptions import (
    BranchCreationError,
    DataFileNotFoundError,
    DownloadError,
    FileUploadError,
    MetadataNotFoundError,
    UploadedFileError,
)
from dumb_datasets.transfer import setup_hf_transfer


def _log_from_exception(message_type: str, exception_cls: type[Exception], **kwargs: Any) -> None:
    """Helper function to create and log a message using an exception object.

    This pattern avoids the TRY003 lint error by using exceptions for messages.

    Args:
        message_type: Log message type ('debug', 'info', 'warning', 'error')
        exception_cls: Exception class to instantiate
        **kwargs: Arguments to pass to the exception constructor
    """
    exc = exception_cls(**kwargs)
    if message_type == "debug":
        logger.debug(str(exc))
    elif message_type == "info":
        logger.info(str(exc))
    elif message_type == "warning":
        logger.warning(str(exc))
    elif message_type == "error":
        logger.error(str(exc))


class HubAPI:
    """wrapper around huggingface hub api with simplified interface."""

    def __init__(self, token: Optional[str] = None) -> None:
        """initialize hub api.

        args:
            token: huggingface api token (defaults to token from config)
        """
        config = get_config()
        self.token = token or config.api_token

        # ensure hf-transfer is enabled if configured
        if config.force_hf_transfer:
            setup_hf_transfer(True)

        # setup api
        self.api = self._create_api()

    def _create_api(self) -> HfApi:
        """create and authenticate with hf api."""
        api = HfApi(token=self.token)
        # attempt authentication if token is provided
        if self.token:
            try:
                whoami = api.whoami()
                logger.debug(f"authenticated with hf hub as: {whoami['name']}")
            except Exception as e:
                logger.warning(f"failed to authenticate with hf hub: {e!s}")
        else:
            logger.debug("no token provided, using anonymous access to hf hub")
        return api

    def list_datasets(self) -> Iterable[DatasetInfo]:
        """list datasets from the hub."""
        return self.api.list_datasets()

    def list_models(self) -> Iterable[ModelInfo]:
        """list models from the hub."""
        return self.api.list_models()

    def upload_file(
        self,
        path_or_fileobj: Union[str, Path, bytes, Any],
        path_in_repo: str,
        repo_id: str,
        repo_type: str = "dataset",
        **kwargs: Any,
    ) -> str:
        """upload a file to the hub.

        args:
            path_or_fileobj: local path or file-like object
            path_in_repo: path to store file in repo
            repo_id: repo id on hub
            repo_type: repo type ('dataset' or 'model')
            **kwargs: additional args for hf api upload_file

        returns:
            url to uploaded file
        """
        # explicitly cast the return value to str
        return cast(
            str,
            self.api.upload_file(
                path_or_fileobj=path_or_fileobj,
                path_in_repo=path_in_repo,
                repo_id=repo_id,
                repo_type=repo_type,
                **kwargs,
            ),
        )

    def _get_worker_id(self) -> str:
        """generate a stable worker id for the current process.

        returns:
            worker id hash string
        """
        # create a hash based on hostname and pid for stable worker identification
        host = os.uname().nodename
        pid = os.getpid()
        # Using SHA256 instead of MD5 for security reasons
        worker_hash = hashlib.sha256(f"{host}:{pid}".encode()).hexdigest()[:6]
        return worker_hash

    def _ensure_intermediates_branch(self, repo_id: str, repo_type: str = "dataset") -> None:
        """ensure intermediates branch exists in the repository.

        args:
            repo_id: repo id on hub
            repo_type: repo type ('dataset' or 'model')
        """
        try:
            # check if branch exists first to avoid unnecessary operations
            self.api.list_repo_refs(repo_id=repo_id, repo_type=repo_type)
        except Exception:
            # branch might not exist, try to create it
            try:
                create_branch(repo_id=repo_id, branch="intermediates", repo_type=repo_type, token=self.token)
                logger.debug(f"created 'intermediates' branch in {repo_id}")
            except Exception as e:
                if "branch already exists" not in str(e).lower():
                    raise BranchCreationError() from e

    def push_intermediate_data(
        self,
        local_path: Optional[str] = None,
        repo_id: str = "",
        token: Optional[str] = None,
        prefix: str = "intermediates",
        date_folder: bool = True,
        **kwargs: Any,
    ) -> str:
        """upload a local file (.jsonl or similar) to intermediates branch.

        automatically organizes by date and worker id to prevent collisions.

        args:
            local_path: path to partial file; defaults to "data.jsonl" if None
            repo_id: huggingface repo id
            token: hf token (overrides instance token if provided)
            prefix: folder prefix in repo (default: "intermediates")
            date_folder: if true, place in prefix/YYYYMMDD/ (default: True)
            **kwargs: additional args for upload_file

        returns:
            url to uploaded file
        """
        if not repo_id:
            raise ValueError("repo_id must be specified")

        # use provided token or fallback to instance token
        use_token = token or self.token

        # default to data.jsonl if no path provided
        if local_path is None:
            local_path = "data.jsonl"

        # ensure the file exists
        if not os.path.isfile(local_path):
            raise DataFileNotFoundError(path=local_path)

        # ensure intermediates branch exists
        self._ensure_intermediates_branch(repo_id=repo_id, repo_type="dataset")

        # generate destination path
        worker_id = self._get_worker_id()

        # count files already uploaded by this worker
        counter = kwargs.pop("counter", 1)

        # build the path in repo
        repo_path_parts = [prefix]

        # add date folder if requested
        if date_folder:
            today = datetime.datetime.now().strftime("%Y%m%d")
            repo_path_parts.append(today)

        # create filename with worker id and counter
        filename = f"worker_{worker_id}_{counter:06d}.jsonl"
        repo_path_parts.append(filename)

        path_in_repo = "/".join(repo_path_parts)

        # try to upload, handling potential collisions
        try:
            return self.upload_file(
                path_or_fileobj=local_path,
                path_in_repo=path_in_repo,
                repo_id=repo_id,
                repo_type="dataset",
                revision="intermediates",
                token=use_token,
                **kwargs,
            )
        except Exception as e:
            if "file already exists" in str(e).lower():
                # Create a new filename with a suffix
                suffix = uuid.uuid4().hex[:4]
                filename = f"worker_{worker_id}_{counter:06d}_{suffix}.jsonl"
                repo_path_parts[-1] = filename
                new_path = "/".join(repo_path_parts)

                # Try again with the new path without logging
                return self.upload_file(
                    path_or_fileobj=local_path,
                    path_in_repo=new_path,
                    repo_id=repo_id,
                    repo_type="dataset",
                    revision="intermediates",
                    token=use_token,
                    **kwargs,
                )
            else:
                # other error, re-raise
                raise

    @contextmanager
    def _temp_jsonl_file(self) -> Generator[tuple[str, list[Dict[str, Any]]], None, None]:
        """context manager that creates a temporary jsonl file.

        yields:
            path to temporary file and a list to store rows
        """
        with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            path = f.name
            rows: list[Dict[str, Any]] = []

            try:
                yield path, rows
            finally:
                # write any pending rows
                if rows:
                    with open(path, "w") as out_file:
                        for row in rows:
                            out_file.write(json.dumps(row) + "\n")

                # cleanup
                try:
                    os.unlink(path)
                except Exception as e:
                    logger.warning(f"failed to cleanup temporary file: {e!s}")

    def _download_intermediates(
        self, repo_id: str, token: Optional[str] = None, temp_dir: str = "", **kwargs: Any
    ) -> str:
        """download the intermediates branch to a temporary directory.

        args:
            repo_id: huggingface repo id
            token: hf token (overrides instance token if provided)
            temp_dir: directory to download to
            **kwargs: additional args for snapshot_download

        returns:
            path to downloaded repository
        """
        try:
            repo_dir = snapshot_download(
                repo_id=repo_id,
                revision="intermediates",
                repo_type="dataset",
                token=token or self.token,
                local_dir=temp_dir,
                **kwargs,
            )

            logger.debug(f"downloaded intermediates branch to {repo_dir}")
            return repo_dir
        except Exception as e:
            raise DownloadError(repo_id=repo_id, branch="intermediates") from e

    def _find_jsonl_files(
        self, repo_dir: str, prefix: str, processed_files: set[str]
    ) -> tuple[list[tuple[str, str]], dict[str, Any]]:
        """find jsonl files in the repo that need processing.

        args:
            repo_dir: path to repository directory
            prefix: folder prefix to look in
            processed_files: set of already processed file paths

        returns:
            tuple of (files_to_process, results_dict)
        """
        results: Dict[str, Any] = {
            "files_processed": 0,
            "rows_processed": 0,
            "rows_after_dedup": 0,
            "output_file": "",
        }

        # find all jsonl files in the prefix directory
        prefix_dir = os.path.join(repo_dir, prefix)
        if not os.path.exists(prefix_dir):
            logger.warning(f"prefix directory '{prefix}' not found in intermediates branch")
            return [], results

        all_jsonl_files = []
        for root, _, files in os.walk(prefix_dir):
            for file in files:
                if file.endswith(".jsonl"):
                    file_path = os.path.join(root, file)
                    # get path relative to repo root for metadata tracking
                    rel_path = os.path.relpath(file_path, repo_dir)
                    all_jsonl_files.append((file_path, rel_path))

        # filter out already processed files
        files_to_process = []
        for file_path, rel_path in all_jsonl_files:
            if rel_path in processed_files:
                logger.debug(f"skipping already processed file: {rel_path}")
            else:
                files_to_process.append((file_path, rel_path))

        return files_to_process, results

    def _process_jsonl_files(
        self,
        files_to_process: list[tuple[str, str]],
        output_file: str,
        deduplicate: bool = True,
        dedup_key: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ) -> tuple[int, int, set[str], set]:
        """process jsonl files, combining and deduplicating them.

        args:
            files_to_process: list of (file_path, rel_path) tuples
            output_file: path to write merged output
            deduplicate: whether to deduplicate rows
            dedup_key: function to extract key for deduplication

        returns:
            tuple of (row_count, processed_files_count, processed_files, seen_keys)
        """
        seen = set()
        row_count = 0
        processed_files_set = set()

        with open(output_file, "w") as outf:
            for file_path, rel_path in files_to_process:
                logger.debug(f"processing file: {rel_path}")
                try:
                    with open(file_path) as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue

                            try:
                                row = json.loads(line)
                                row_count += 1

                                # handle deduplication
                                if deduplicate:
                                    # use custom key function if provided, else use entire row as key
                                    key = dedup_key(row) if dedup_key is not None else json.dumps(row, sort_keys=True)

                                    if key in seen:
                                        continue
                                    seen.add(key)

                                # write to output file
                                outf.write(json.dumps(row) + "\n")
                            except json.JSONDecodeError:
                                logger.warning(f"invalid json in {rel_path}: {line}")
                except Exception as e:
                    logger.error(f"error processing {rel_path}: {e!s}")

                # mark file as processed
                processed_files_set.add(rel_path)

        return row_count, len(processed_files_set), processed_files_set, seen

    def _upload_results(
        self,
        output_file: str,
        output_file_name: str,
        repo_id: str,
        aggregator_branch: str,
        push_to_main: bool = True,
        token: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """upload merged results to specified branches.

        args:
            output_file: local path to the merged file
            output_file_name: name for the file in the repository
            repo_id: huggingface repo id
            aggregator_branch: branch for aggregated results
            push_to_main: whether to push to main after merging
            token: hf token (overrides instance token if provided)
            **kwargs: additional args for upload_file
        """
        try:
            # Upload to aggregator branch
            self.upload_file(
                path_or_fileobj=output_file,
                path_in_repo=output_file_name,
                repo_id=repo_id,
                repo_type="dataset",
                revision=aggregator_branch,
                token=token or self.token,
                create_pr=False,
                **kwargs,
            )

            # Log using helper function
            _log_from_exception(
                "info", UploadedFileError, file_name=output_file_name, path=f"{aggregator_branch}/{output_file_name}"
            )

            # push to main if requested
            if push_to_main:
                self.upload_file(
                    path_or_fileobj=output_file,
                    path_in_repo=output_file_name,
                    repo_id=repo_id,
                    repo_type="dataset",
                    revision="main",
                    token=token or self.token,
                    create_pr=False,
                    **kwargs,
                )

                # Log using helper function
                _log_from_exception(
                    "info", UploadedFileError, file_name=output_file_name, path=f"main/{output_file_name}"
                )

        except Exception as e:
            # Use a custom exception for error handling
            raise FileUploadError(path=output_file_name, repo_id=repo_id, branch=aggregator_branch) from e

    def merge_intermediate_data(
        self,
        repo_id: str,
        token: Optional[str] = None,
        prefix: str = "intermediates",
        aggregator_branch: str = "aggregator_output",
        push_to_main: bool = True,
        deduplicate: bool = True,
        dedup_key: Optional[Callable[[Dict[str, Any]], Any]] = None,
        remember_merged: bool = True,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """merge intermediate data files from intermediates branch.

        1. downloads all partial files from intermediates branch/prefix
        2. concatenates them into a single dataset
        3. deduplicates if requested
        4. commits merged data to aggregator_branch
        5. optionally pushes to main branch

        args:
            repo_id: huggingface repo id
            token: hf token (overrides instance token if provided)
            prefix: folder prefix in repo (default: "intermediates")
            aggregator_branch: branch for aggregated results
            push_to_main: whether to push to main after merging
            deduplicate: whether to deduplicate rows
            dedup_key: function to extract key for deduplication (default: entire row)
            remember_merged: track which partials were merged
            **kwargs: additional args for download/upload

        returns:
            dict with merge results (files merged, rows processed, etc)
        """
        if not repo_id:
            raise ValueError("repo_id must be specified")

        # use provided token or fallback to instance token
        use_token = token or self.token

        results: Dict[str, Any] = {
            "files_processed": 0,
            "rows_processed": 0,
            "rows_after_dedup": 0,
            "output_file": "",
        }

        # fetch metadata of already processed files if remember_merged is True
        metadata_file = ".merged_metadata.json"
        processed_files = set()

        if remember_merged:
            try:
                metadata_path = download_file(
                    repo_id=repo_id,
                    filename=metadata_file,
                    repo_type="dataset",
                    revision=aggregator_branch,
                    token=use_token,
                    **kwargs,
                )

                with open(metadata_path) as f:
                    metadata = json.load(f)
                    processed_files = set(metadata.get("processed_files", []))

                logger.debug(f"loaded {len(processed_files)} previously processed files")
            except Exception as e:
                raise MetadataNotFoundError() from e

        # create temporary dir for downloaded files
        with TemporaryDirectory() as temp_dir:
            # download entire intermediates branch
            try:
                repo_dir = self._download_intermediates(repo_id=repo_id, token=use_token, temp_dir=temp_dir, **kwargs)
            except DownloadError:
                # for metadata not found and download errors, return empty results
                return results

            # find files that need processing
            files_to_process, results = self._find_jsonl_files(repo_dir, prefix, processed_files)

            if files_to_process:
                # process the files
                output_file = os.path.join(temp_dir, "merged_data.jsonl")
                row_count, files_processed, new_processed_files, seen = self._process_jsonl_files(
                    files_to_process=files_to_process,
                    output_file=output_file,
                    deduplicate=deduplicate,
                    dedup_key=dedup_key,
                )

                # update results
                results["files_processed"] = files_processed
                results["rows_processed"] = row_count
                if deduplicate:
                    results["rows_after_dedup"] = len(seen)
                else:
                    results["rows_after_dedup"] = row_count

                # update metadata if remember_merged is True
                if remember_merged:
                    processed_files.update(new_processed_files)
                    metadata_path = os.path.join(temp_dir, metadata_file)
                    with open(metadata_path, "w") as f:
                        json.dump({"processed_files": list(processed_files)}, f)

                    # upload metadata to aggregator branch
                    self.upload_file(
                        path_or_fileobj=metadata_path,
                        path_in_repo=metadata_file,
                        repo_id=repo_id,
                        repo_type="dataset",
                        revision=aggregator_branch,
                        token=use_token,
                        create_pr=False,
                        **kwargs,
                    )

                # upload merged data to aggregator branch
                output_file_name = f"merged_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
                results["output_file"] = output_file_name

                # upload results
                self._upload_results(
                    output_file=output_file,
                    output_file_name=output_file_name,
                    repo_id=repo_id,
                    aggregator_branch=aggregator_branch,
                    push_to_main=push_to_main,
                    token=use_token,
                    **kwargs,
                )

                return results
            else:
                # No files to process
                logger.info("no new files to process")
                return results


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def download_file(
    repo_id: str,
    filename: str,
    repo_type: str = "dataset",
    revision: Optional[str] = None,
    cache_dir: Optional[str] = None,
    **kwargs: Any,
) -> str:
    """download a single file from the hub with retries.

    args:
        repo_id: repo id on hub
        filename: file to download
        repo_type: repo type ('dataset' or 'model')
        revision: specific revision to download
        cache_dir: local cache directory
        **kwargs: additional args for hf_hub_download

    returns:
        path to downloaded file
    """
    config = get_config()
    if cache_dir is None and config.cache_dir is not None:
        cache_dir = str(config.cache_dir)
    if config.api_token:
        kwargs["token"] = config.api_token

    # ensure hf-transfer is enabled if configured
    if config.force_hf_transfer:
        setup_hf_transfer(True)

    try:
        logger.debug(f"downloading file: {filename} from {repo_id}")
        return hf_hub_download(
            repo_id=repo_id, filename=filename, repo_type=repo_type, revision=revision, cache_dir=cache_dir, **kwargs
        )
    except Exception as e:
        logger.error(f"failed to download file: {e!s}")
        raise


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def download_repository(
    repo_id: str,
    repo_type: str = "dataset",
    revision: Optional[str] = None,
    cache_dir: Optional[str] = None,
    **kwargs: Any,
) -> str:
    """download an entire repository from the hub with retries.

    args:
        repo_id: repo id on hub
        repo_type: repo type ('dataset' or 'model')
        revision: specific revision to download
        cache_dir: local cache directory
        **kwargs: additional args for snapshot_download

    returns:
        path to downloaded repository
    """
    config = get_config()
    if cache_dir is None and config.cache_dir is not None:
        cache_dir = str(config.cache_dir)
    if config.api_token:
        kwargs["token"] = config.api_token

    # ensure hf-transfer is enabled if configured
    if config.force_hf_transfer:
        setup_hf_transfer(True)

    try:
        logger.debug(f"downloading repository: {repo_id}")
        return snapshot_download(repo_id=repo_id, repo_type=repo_type, revision=revision, cache_dir=cache_dir, **kwargs)
    except Exception as e:
        logger.error(f"failed to download repository: {e!s}")
        raise


def push_intermediate_data(
    local_path: Optional[str] = None,
    repo_id: str = "",
    token: Optional[str] = None,
    prefix: str = "intermediates",
    date_folder: bool = True,
    **kwargs: Any,
) -> str:
    """upload a local file (.jsonl or similar) to intermediates branch.

    automatically organizes by date and worker id to prevent collisions.

    args:
        local_path: path to partial file; defaults to "data.jsonl" if None
        repo_id: huggingface repo id
        token: hf token
        prefix: folder prefix in repo (default: "intermediates")
        date_folder: if true, place in prefix/YYYYMMDD/ (default: True)
        **kwargs: additional args for upload_file

    returns:
        url to uploaded file
    """
    api = HubAPI(token=token)
    return api.push_intermediate_data(
        local_path=local_path, repo_id=repo_id, token=token, prefix=prefix, date_folder=date_folder, **kwargs
    )


def merge_intermediate_data(
    repo_id: str,
    token: Optional[str] = None,
    prefix: str = "intermediates",
    aggregator_branch: str = "aggregator_output",
    push_to_main: bool = True,
    deduplicate: bool = True,
    dedup_key: Optional[Callable[[Dict[str, Any]], Any]] = None,
    remember_merged: bool = True,
    **kwargs: Any,
) -> Dict[str, Any]:
    """merge intermediate data files from intermediates branch.

    1. downloads all partial files from intermediates branch/prefix
    2. concatenates them into a single dataset
    3. deduplicates if requested
    4. commits merged data to aggregator_branch
    5. optionally pushes to main branch

    args:
        repo_id: huggingface repo id
        token: hf token
        prefix: folder prefix in repo (default: "intermediates")
        aggregator_branch: branch for aggregated results
        push_to_main: whether to push to main after merging
        deduplicate: whether to deduplicate rows
        dedup_key: function to extract key for deduplication (default: entire row)
        remember_merged: track which partials were merged
        **kwargs: additional args for download/upload

    returns:
        dict with merge results (files merged, rows processed, etc)
    """
    api = HubAPI(token=token)
    return api.merge_intermediate_data(
        repo_id=repo_id,
        token=token,
        prefix=prefix,
        aggregator_branch=aggregator_branch,
        push_to_main=push_to_main,
        deduplicate=deduplicate,
        dedup_key=dedup_key,
        remember_merged=remember_merged,
        **kwargs,
    )
