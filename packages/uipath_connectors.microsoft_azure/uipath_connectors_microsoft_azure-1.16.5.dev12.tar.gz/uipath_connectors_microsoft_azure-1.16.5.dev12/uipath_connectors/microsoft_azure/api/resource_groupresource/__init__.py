from .create_resource_group import sync as create_resource_group
from .create_resource_group import asyncio as create_resource_group_async
from .delete_resource_group import sync as delete_resource_group
from .delete_resource_group import asyncio as delete_resource_group_async

__all__ = [
    "create_resource_group",
    "create_resource_group_async",
    "delete_resource_group",
    "delete_resource_group_async",
]
