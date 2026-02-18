from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .component import button

try:
    __version__ = version("hyperlink_button")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["button", "__version__"]
