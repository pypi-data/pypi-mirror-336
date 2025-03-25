from typing import Any
from .api import SapOdata  # type: ignore
from .models import *  # type: ignore


def register_connector(connections: Any):
    """Register the sap_odata connector."""
    connections.sap_odata = lambda instance_id: SapOdata(
        instance_id=instance_id, client=connections.client
    )
