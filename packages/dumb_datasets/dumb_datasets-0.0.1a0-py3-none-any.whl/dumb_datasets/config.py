"""Configuration module for dumb-datasets."""

from typing import Optional
import os
from pathlib import Path

from loguru import logger
from pydantic import BaseModel
from dotenv import load_dotenv

# load env vars
load_dotenv()


class Config(BaseModel):
    """Global config for dumb-datasets."""

    cache_dir: Optional[Path] = None
    api_token: Optional[str] = None
    verbose: bool = False


# global config singleton
_config = Config(
    cache_dir=os.environ.get("DUMB_DATASETS_CACHE_DIR", None),
    api_token=os.environ.get("HF_TOKEN", None),
    verbose=os.environ.get("DUMB_DATASETS_VERBOSE", "").lower() == "true"
)


def set_cache_dir(path: str) -> None:
    """Set the cache directory for datasets.

    Args:
        path: Directory path for caching datasets
    """
    _config.cache_dir = Path(path)
    logger.debug(f"cache dir set to {path}")


def set_api_token(token: str) -> None:
    """Set the HuggingFace API token.

    Args:
        token: HuggingFace API token
    """
    _config.api_token = token
    # mask token in logs
    masked = token[:4] + "..." + token[-4:] if len(token) > 8 else "****"
    logger.debug(f"api token set to {masked}")


def get_config() -> Config:
    """Get the current configuration."""
    return _config