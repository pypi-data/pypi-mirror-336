"""Configuration module for dumb-datasets."""

import os
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv  # type: ignore[import-not-found]
from loguru import logger  # type: ignore[import-not-found]
from pydantic import BaseModel

# load env vars
load_dotenv()


class Config(BaseModel):  # type: ignore[misc]
    """Global config for dumb-datasets."""

    cache_dir: Optional[Path] = None
    api_token: Optional[str] = None
    force_hf_transfer: bool = True
    verbose: bool = False


# get cache dir from env var if it exists
cache_dir_env = os.environ.get("DUMB_DATASETS_CACHE_DIR")
cache_dir_path = Path(cache_dir_env) if cache_dir_env else None

# check for HF_TOKEN in environment variables
hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")

# common llm provider api keys that litellm supports
llm_provider_keys = {
    # openai and azure openai
    "OPENAI_API_KEY": None,
    "AZURE_API_KEY": None,
    "AZURE_API_BASE": None,
    "AZURE_API_VERSION": None,
    # anthropic
    "ANTHROPIC_API_KEY": None,
    # google
    "VERTEX_PROJECT": None,
    "VERTEX_LOCATION": None,
    # aws
    "AWS_ACCESS_KEY_ID": None,
    "AWS_SECRET_ACCESS_KEY": None,
    "AWS_REGION_NAME": None,
    # other major providers
    "COHERE_API_KEY": None,
    "REPLICATE_API_KEY": None,
    "HUGGINGFACE_API_KEY": None,
    "TOGETHERAI_API_KEY": None,
    "MISTRAL_API_KEY": None,
    "CLOUDFLARE_API_KEY": None,
    "PERPLEXITY_API_KEY": None,
    "GROQ_API_KEY": None,
}

# load all available api keys from env
for key in llm_provider_keys:
    value = os.getenv(key)
    if value is not None:  # explicit None check for type safety
        os.environ[key] = value
        # mask key in logs for security
        masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "****"
        logger.debug(f"loaded {key}: {masked}")

# global config singleton
_config = Config(
    cache_dir=cache_dir_path,
    api_token=hf_token,
    force_hf_transfer=os.environ.get("HF_HUB_ENABLE_HF_TRANSFER", "1").lower() in ("1", "true", "yes"),
    verbose=os.environ.get("DUMB_DATASETS_VERBOSE", "").lower() == "true",
)


def set_cache_dir(path: Union[str, Path]) -> None:
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


def enable_hf_transfer(enabled: bool = True) -> None:
    """Enable or disable HF Transfer for faster downloads.

    When enabled, hf-transfer will be used for all downloads from the Hub.
    This is enabled by default.

    Args:
        enabled: Whether to enable HF Transfer
    """
    from dumb_datasets.transfer import setup_hf_transfer

    _config.force_hf_transfer = enabled
    setup_hf_transfer(enabled)
    logger.debug(f"hf transfer {'enabled' if enabled else 'disabled'}")


def get_config() -> Config:
    """Get the current configuration."""
    return _config
