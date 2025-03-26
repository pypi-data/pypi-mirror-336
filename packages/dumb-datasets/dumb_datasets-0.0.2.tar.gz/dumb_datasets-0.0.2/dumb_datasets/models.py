"""models module for dumb-datasets.

defines data models for representing dataset metadata using pydantic.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel  # type: ignore[import-not-found]


class DatasetModel(BaseModel):
    """model representing dataset information, inspired by huggingface's datasetinfo."""

    features: dict[str, Any]
    num_rows: int
    description: Optional[str] = None
    citation: Optional[str] = None
    homepage: Optional[str] = None
    license: Optional[str] = None
    splits: Optional[dict[str, dict[str, Any]]] = None
    download_size: Optional[int] = None
    dataset_size: Optional[int] = None

    @classmethod
    def from_dataset(cls, dataset: Any) -> DatasetModel:
        """create a datasetmodel instance from a dataset's info.

        attempts to extract common dataset info fields from various sources.
        """
        info = dataset.info()

        # extract split info if available
        splits = None
        if isinstance(info, dict) and any(k in info for k in ["train", "test", "validation"]):
            # this is likely a dataset dict with splits
            splits = {
                k: v
                for k, v in info.items()
                if k not in ["features", "num_rows", "description", "citation", "homepage"]
            }

        return cls(
            features=info.get("features", {}),
            num_rows=info.get("num_rows", 0),
            description=info.get("description"),
            citation=info.get("citation"),
            homepage=info.get("homepage"),
            license=info.get("license"),
            splits=splits,
            download_size=info.get("download_size"),
            dataset_size=info.get("dataset_size"),
        )


class DatasetInfo(BaseModel):  # type: ignore[misc]
    """information about a dataset."""

    name: str
    description: str = ""
    features: Dict[str, Any]
    num_rows: int
    homepage: Optional[str] = None
    license: Optional[str] = None
    citation: Optional[str] = None
    splits: Optional[Dict[str, Dict[str, Any]]] = None
    download_size: Optional[int] = None
    dataset_size: Optional[int] = None
