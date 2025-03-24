"""dumb-datasets: a lightweight wrapper around huggingface datasets."""

from dumb_datasets.__version__ import __version__
from dumb_datasets.api import load_dataset, Dataset
from dumb_datasets.config import set_cache_dir, set_api_token
from dumb_datasets.utils import save_dataset_sample, dataset_schema, sanitize_name
from dumb_datasets.exceptions import DumbDatasetsException
from dumb_datasets.sessions import Session
from dumb_datasets.models import DatasetModel
from dumb_datasets.hooks import add_hook, run_hooks
from dumb_datasets.adapters import register_adapter, get_adapter
from dumb_datasets.features import (
    Features,
    Value,
    ClassLabel,
    Translation,
    Sequence,
    Image,
    Audio,
    infer_features_from_dict,
    save_features,
    load_features,
)

__all__ = [
    # Core functionality
    "load_dataset",
    "Dataset",
    "set_cache_dir",
    "set_api_token",

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

    # Version
    "__version__",
]
