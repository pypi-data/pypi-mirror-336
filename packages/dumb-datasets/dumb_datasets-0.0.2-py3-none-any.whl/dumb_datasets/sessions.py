"""Session module for dumb-datasets.

provides a Session class to manage persistent dataset operations (e.g. caching and authentication).
"""

from typing import Any, Callable, Dict, Optional, cast

from dumb_datasets.api import Dataset, load_dataset
from dumb_datasets.config import enable_hf_transfer, set_api_token, set_cache_dir
from dumb_datasets.hub import HubAPI


class Session:
    """session object for managing dataset operations across multiple calls.

    encapsulates settings like cache directory and authentication token for efficient dataset loading.
    """

    def __init__(
        self, cache_dir: Optional[str] = None, api_token: Optional[str] = None, force_hf_transfer: bool = True
    ) -> None:
        """initialize a new session.

        args:
            cache_dir: directory for caching datasets
            api_token: huggingface api token
            force_hf_transfer: whether to force enable hf-transfer for faster downloads
        """
        if cache_dir:
            set_cache_dir(cache_dir)
        if api_token:
            set_api_token(api_token)

        # always set hf_transfer preference in session init
        enable_hf_transfer(force_hf_transfer)

        # create hub api instance with the token
        self.hub = HubAPI(token=api_token)

    def get_dataset(self, *args: Any, **kwargs: Any) -> Dataset:
        """retrieve a dataset using current session settings.

        all arguments are passed directly to load_dataset.
        """
        return cast(Dataset, load_dataset(*args, **kwargs))

    def download_file(self, *args: Any, **kwargs: Any) -> str:
        """download a file from the hub.

        all arguments are passed directly to hub.download_file.
        """
        from dumb_datasets.hub import download_file

        return download_file(*args, **kwargs)

    def download_repository(self, *args: Any, **kwargs: Any) -> str:
        """download a repository from the hub.

        all arguments are passed directly to hub.download_repository.
        """
        from dumb_datasets.hub import download_repository

        return download_repository(*args, **kwargs)

    def push_intermediate_data(
        self,
        local_path: Optional[str] = None,
        repo_id: str = "",
        prefix: str = "intermediates",
        date_folder: bool = True,
        **kwargs: Any,
    ) -> str:
        """upload a local file (.jsonl or similar) to intermediates branch.

        automatically organizes by date and worker id to prevent collisions.
        uses the session's authentication token.

        args:
            local_path: path to partial file; defaults to "data.jsonl" if None
            repo_id: huggingface repo id
            prefix: folder prefix in repo (default: "intermediates")
            date_folder: if true, place in prefix/YYYYMMDD/ (default: True)
            **kwargs: additional args for upload_file

        returns:
            url to uploaded file
        """
        return self.hub.push_intermediate_data(
            local_path=local_path, repo_id=repo_id, prefix=prefix, date_folder=date_folder, **kwargs
        )

    def merge_intermediate_data(
        self,
        repo_id: str,
        prefix: str = "intermediates",
        aggregator_branch: str = "aggregator_output",
        push_to_main: bool = True,
        deduplicate: bool = True,
        dedup_key: Optional[Callable[[Dict[str, Any]], Any]] = None,
        remember_merged: bool = True,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """merge intermediate data files from intermediates branch.

        uses the session's authentication token.

        1. downloads all partial files from intermediates branch/prefix
        2. concatenates them into a single dataset
        3. deduplicates if requested
        4. commits merged data to aggregator_branch
        5. optionally pushes to main branch

        args:
            repo_id: huggingface repo id
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
        return self.hub.merge_intermediate_data(
            repo_id=repo_id,
            prefix=prefix,
            aggregator_branch=aggregator_branch,
            push_to_main=push_to_main,
            deduplicate=deduplicate,
            dedup_key=dedup_key,
            remember_merged=remember_merged,
            **kwargs,
        )
