from .reset_password import sync as reset_password
from .reset_password import asyncio as reset_password_async

__all__ = [
    "reset_password",
    "reset_password_async",
]
