from .delete_nsg import sync as delete_nsg
from .delete_nsg import asyncio as delete_nsg_async
from .list_ns_gs import sync as list_ns_gs
from .list_ns_gs import asyncio as list_ns_gs_async

__all__ = [
    "delete_nsg",
    "delete_nsg_async",
    "list_ns_gs",
    "list_ns_gs_async",
]
