from .get_virtual_machine_list import sync as get_virtual_machine_list
from .get_virtual_machine_list import asyncio as get_virtual_machine_list_async

__all__ = [
    "get_virtual_machine_list",
    "get_virtual_machine_list_async",
]
