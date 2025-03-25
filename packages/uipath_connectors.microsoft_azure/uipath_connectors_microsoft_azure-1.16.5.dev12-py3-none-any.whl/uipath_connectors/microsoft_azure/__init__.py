from typing import Any
from .api import MicrosoftAzure  # type: ignore
from .models import *  # type: ignore


def register_connector(connections: Any):
    """Register the microsoft_azure connector."""
    connections.microsoft_azure = lambda instance_id: MicrosoftAzure(
        instance_id=instance_id, client=connections.client
    )
