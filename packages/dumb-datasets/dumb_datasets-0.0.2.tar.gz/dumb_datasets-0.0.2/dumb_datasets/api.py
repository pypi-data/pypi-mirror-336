"""API module for dumb_datasets package.
Provides core functionality like dataset loading and wrapping.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union, cast

import datasets  # type: ignore[import-untyped]
from datasets import Dataset as HFDataset  # type: ignore[import-untyped]
from datasets import DatasetDict as HFDatasetDict  # type: ignore[import-untyped]
from datasets.utils.logging import set_verbosity_error, set_verbosity_info  # type: ignore[import-untyped]
from loguru import logger  # type: ignore[import-not-found]
from tenacity import retry, stop_after_attempt, wait_exponential  # type: ignore[import-not-found]

from dumb_datasets.config import get_config
from dumb_datasets.transfer import setup_hf_transfer

# configure huggingface datasets logger based on our verbosity
if get_config().verbose:
    set_verbosity_info()
else:
    set_verbosity_error()

# force enable hf-transfer if configured (which is the default)
# this has to be done before any imports from huggingface_hub
if get_config().force_hf_transfer:
    setup_hf_transfer(True)


T = TypeVar("T")


class Dataset:
    """Wrapper around HuggingFace Dataset with additional functionality."""

    def __init__(self, dataset: Union[HFDataset, HFDatasetDict]) -> None:  # type: ignore[no-any-unimported]
        """Initialize the dataset wrapper.

        Args:
            dataset: HuggingFace dataset object
        """
        self._dataset = dataset

    @property
    def raw(self) -> Union[HFDataset, HFDatasetDict]:  # type: ignore[no-any-unimported]
        """Get the raw HuggingFace dataset."""
        return self._dataset

    def info(self) -> Dict[str, Any]:
        """Get dataset info as a dictionary."""
        if isinstance(self._dataset, HFDataset):
            info = self._dataset.info
            return {
                "features": self._dataset.features,
                "num_rows": len(self._dataset),
                "description": info.description,
                "citation": info.citation,
                "homepage": info.homepage,
                "license": getattr(info, "license", None),
                "version": getattr(info, "version", None),
                "download_size": getattr(info, "download_size", None),
                "dataset_size": getattr(info, "dataset_size", None),
            }
        else:
            # dataset dict case
            result: Dict[str, Dict[str, Any]] = {}
            for split_name, split_dataset in self._dataset.items():
                info = split_dataset.info
                result[split_name] = {
                    "features": split_dataset.features,
                    "num_rows": len(split_dataset),
                    "description": info.description,
                    "version": getattr(info, "version", None),
                }
            return result

    def map_columns(self, fn: Callable[[Any], Any], columns: List[str]) -> Dataset:
        """Apply a function to specified columns in the dataset.

        Args:
            fn: Function to apply
            columns: List of column names to transform

        Returns:
            New Dataset with transformed columns
        """

        def _apply(example: dict) -> dict:
            for col in columns:
                if col in example:
                    example[col] = fn(example[col])
            return example

        if isinstance(self._dataset, HFDataset):
            return Dataset(self._dataset.map(_apply))
        else:
            return Dataset({k: v.map(_apply) for k, v in self._dataset.items()})

    def filter(self, fn: Callable[[Dict[str, Any]], bool]) -> Dataset:
        """Filter the dataset using a predicate function.

        Args:
            fn: Predicate function that returns True for rows to keep

        Returns:
            New filtered Dataset
        """
        if isinstance(self._dataset, HFDataset):
            return Dataset(self._dataset.filter(fn))
        else:
            return Dataset({k: v.filter(fn) for k, v in self._dataset.items()})

    def select(self, indices: Union[List[int], range]) -> Dataset:
        """Select specific rows by indices.

        Args:
            indices: List or range of indices to select

        Returns:
            New Dataset with only the selected rows
        """
        if isinstance(self._dataset, HFDataset):
            return Dataset(self._dataset.select(indices))
        else:
            return Dataset({k: v.select(indices) for k, v in self._dataset.items()})

    def shuffle(self, seed: Optional[int] = None) -> Dataset:
        """Randomly shuffle the dataset.

        Args:
            seed: Random seed for reproducibility

        Returns:
            New shuffled Dataset
        """
        if isinstance(self._dataset, HFDataset):
            return Dataset(self._dataset.shuffle(seed=seed))
        else:
            return Dataset({k: v.shuffle(seed=seed) for k, v in self._dataset.items()})

    def to_pandas(self) -> Any:
        """Convert the dataset to pandas DataFrame(s)."""
        if isinstance(self._dataset, HFDataset):
            return self._dataset.to_pandas()
        else:
            return {k: v.to_pandas() for k, v in self._dataset.items()}

    def to_dict(self) -> Dict[str, List[Any]]:
        """Convert the dataset to a dictionary of lists."""
        if isinstance(self._dataset, HFDataset):
            # Cast to explicit return type
            return cast(Dict[str, List[Any]], self._dataset.to_dict())
        else:
            # For dataset dict, create result with proper typing
            result: Dict[str, List[Any]] = {}
            for k, v in self._dataset.items():
                # Cast each dict value to list[Any]
                result[k] = cast(List[Any], v.to_dict())
            return result

    def __getitem__(self, key: Any) -> Any:
        """Retrieve item or subset from the dataset."""
        result = self._dataset[key]
        if isinstance(result, (HFDataset, HFDatasetDict)):
            return Dataset(result)
        return result

    def __len__(self) -> int:
        """Get the number of examples in the dataset."""
        if isinstance(self._dataset, HFDataset):
            return len(self._dataset)
        # For DatasetDict, return total across all splits
        return sum(len(ds) for ds in self._dataset.values())

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Iterate through examples in the dataset."""
        if isinstance(self._dataset, HFDataset):
            for example in self._dataset:
                yield example
        else:
            # Not ideal to concatenate splits, but provides a simple iteration interface
            for split in self._dataset.values():
                for example in split:
                    yield example


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def load_dataset(
    path: str,
    name: Optional[str] = None,
    split: Optional[str] = None,
    cache_dir: Optional[str] = None,
    download_mode: Optional[str] = None,
    trust_remote_code: bool = False,
    **kwargs: Any,
) -> Dataset:
    """Load a dataset with retries and error handling.

    Args:
        path: Dataset identifier or path
        name: Configuration name
        split: Specific split to load
        cache_dir: Custom cache directory
        download_mode: Mode for dataset downloads ('reuse_dataset_if_exists' or 'force_redownload')
        trust_remote_code: Whether to trust remote code when loading the dataset
        **kwargs: Additional options for datasets.load_dataset

    Returns:
        A wrapped Dataset instance
    """
    config = get_config()
    if cache_dir is None and config.cache_dir is not None:
        cache_dir = str(config.cache_dir)
    if config.api_token:
        os.environ["HF_TOKEN"] = config.api_token

    # ensure hf-transfer is enabled if configured
    if config.force_hf_transfer:
        setup_hf_transfer(True)

    try:
        logger.debug(f"loading dataset: {path}" + (f"/{name}" if name else ""))
        ds = datasets.load_dataset(
            path=path,
            name=name,
            split=split,
            cache_dir=cache_dir,
            download_mode=download_mode,
            trust_remote_code=trust_remote_code,
            **kwargs,
        )
        return Dataset(ds)
    except Exception as e:
        logger.error(f"failed to load dataset: {e!s}")
        raise
