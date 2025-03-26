"""dumb-datasets: a lightweight wrapper around huggingface datasets."""

from dumb_datasets.__version__ import __version__
from dumb_datasets.adapters import get_adapter, register_adapter
from dumb_datasets.api import Dataset, load_dataset
from dumb_datasets.config import enable_hf_transfer, set_api_token, set_cache_dir
from dumb_datasets.exceptions import DumbDatasetsException
from dumb_datasets.features import (
    Audio,
    ClassLabel,
    Features,
    Image,
    Sequence,
    Translation,
    Value,
    infer_features_from_dict,
    load_features,
    save_features,
)
from dumb_datasets.hooks import add_hook, run_hooks
from dumb_datasets.hub import (
    HubAPI,
    download_file,
    download_repository,
    merge_intermediate_data,
    push_intermediate_data,
)
from dumb_datasets.models import DatasetModel
from dumb_datasets.sessions import Session
from dumb_datasets.transfer import is_hf_transfer_available
from dumb_datasets.utils import dataset_schema, sanitize_name, save_dataset_sample

__all__ = [
    # Core functionality
    "load_dataset",
    "Dataset",
    "set_cache_dir",
    "set_api_token",
    "enable_hf_transfer",
    # Utilities
    "save_dataset_sample",
    "dataset_schema",
    "sanitize_name",
    # Models and exceptions
    "DumbDatasetsException",
    "Session",
    "DatasetModel",
    # Extension points
    "add_hook",
    "run_hooks",
    "register_adapter",
    "get_adapter",
    # Features
    "Features",
    "Value",
    "ClassLabel",
    "Translation",
    "Sequence",
    "Image",
    "Audio",
    "infer_features_from_dict",
    "save_features",
    "load_features",
    # Hub integration
    "HubAPI",
    "download_file",
    "download_repository",
    "is_hf_transfer_available",
    "push_intermediate_data",
    "merge_intermediate_data",
    # Version
    "__version__",
]
