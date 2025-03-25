from .suspend_members import sync as suspend_members
from .suspend_members import asyncio as suspend_members_async

__all__ = [
    "suspend_members",
    "suspend_members_async",
]
