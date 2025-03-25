from typing import Any
from .api import SapBapi  # type: ignore
from .models import *  # type: ignore


def register_connector(connections: Any):
    """Register the sap_bapi connector."""
    connections.sap_bapi = lambda instance_id: SapBapi(
        instance_id=instance_id, client=connections.client
    )
