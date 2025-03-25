from .delete_network_interface import sync as delete_network_interface
from .delete_network_interface import asyncio as delete_network_interface_async
from .get_network_interface import sync as get_network_interface
from .get_network_interface import asyncio as get_network_interface_async

__all__ = [
    "delete_network_interface",
    "delete_network_interface_async",
    "get_network_interface",
    "get_network_interface_async",
]
