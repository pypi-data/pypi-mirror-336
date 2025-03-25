from .file_uploads import sync as file_uploads
from .file_uploads import asyncio as file_uploads_async

__all__ = [
    "file_uploads",
    "file_uploads_async",
]
