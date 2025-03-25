from .get_virtual_machine import sync as get_virtual_machine
from .get_virtual_machine import asyncio as get_virtual_machine_async

__all__ = [
    "get_virtual_machine",
    "get_virtual_machine_async",
]
