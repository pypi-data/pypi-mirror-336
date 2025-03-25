from .create_nsg import sync as create_nsg
from .create_nsg import asyncio as create_nsg_async
from .get_nsg import sync as get_nsg
from .get_nsg import asyncio as get_nsg_async

__all__ = [
    "create_nsg",
    "create_nsg_async",
    "get_nsg",
    "get_nsg_async",
]
