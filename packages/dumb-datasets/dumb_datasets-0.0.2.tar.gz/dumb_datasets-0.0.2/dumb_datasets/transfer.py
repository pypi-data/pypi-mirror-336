"""transfer module for handling hf-transfer integration.

provides utilities for checking and enabling hf-transfer for faster downloads.
"""

import importlib.util
import os

from loguru import logger  # type: ignore[import-not-found]


def is_hf_transfer_available() -> bool:
    """check if hf-transfer is installed.

    returns:
        true if hf-transfer is installed, false otherwise
    """
    return importlib.util.find_spec("hf_transfer") is not None


def setup_hf_transfer(enabled: bool = True) -> None:
    """setup hf-transfer for use with huggingface_hub.

    args:
        enabled: whether to enable hf-transfer
    """
    if not enabled:
        if "HF_HUB_ENABLE_HF_TRANSFER" in os.environ:
            os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"
        return

    # check if hf-transfer is available
    if not is_hf_transfer_available():
        logger.warning(
            "hf-transfer is enabled but not installed. " "Install with 'pip install hf-transfer' for faster downloads."
        )
        return

    # import hf_transfer to satisfy deptry
    try:
        # Direct import to satisfy deptry (but use in a try block)
        import hf_transfer  # type: ignore[import-untyped] # noqa: F401

        # set environment variable to enable hf-transfer
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
        logger.debug("hf-transfer enabled for faster downloads")
    except ImportError:
        logger.warning("failed to import hf-transfer, falling back to standard download")
