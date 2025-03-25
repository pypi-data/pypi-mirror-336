from typing import Any
from .api import MicrosoftAzureactivedirectory  # type: ignore
from .models import *  # type: ignore


def register_connector(connections: Any):
    """Register the microsoft_azureactivedirectory connector."""
    connections.microsoft_azureactivedirectory = (
        lambda instance_id: MicrosoftAzureactivedirectory(
            instance_id=instance_id, client=connections.client
        )
    )
