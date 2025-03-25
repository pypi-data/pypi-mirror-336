from .file_downloads import sync as file_downloads
from .file_downloads import asyncio as file_downloads_async

__all__ = [
    "file_downloads",
    "file_downloads_async",
]
