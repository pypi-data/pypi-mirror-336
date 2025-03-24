"""Session module for dumb-datasets.

provides a Session class to manage persistent dataset operations (e.g. caching and authentication).
"""

from typing import Optional, Any

from dumb_datasets.api import load_dataset, Dataset
from dumb_datasets.config import set_cache_dir, set_api_token


class Session:
    """session object for managing dataset operations across multiple calls.

    encapsulates settings like cache directory and authentication token for efficient dataset loading.
    """

    def __init__(self, cache_dir: Optional[str] = None, api_token: Optional[str] = None) -> None:
        if cache_dir:
            set_cache_dir(cache_dir)
        if api_token:
            set_api_token(api_token)

    def get_dataset(self, *args: Any, **kwargs: Any) -> 'Dataset':
        """retrieve a dataset using current session settings.

        all arguments are passed directly to load_dataset.
        """
        from typing import cast
        return cast('Dataset', load_dataset(*args, **kwargs))