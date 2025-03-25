from typing import Any
from .api import DropboxDropbox  # type: ignore
from .models import *  # type: ignore


def register_connector(connections: Any):
    """Register the dropbox_dropbox connector."""
    connections.dropbox_dropbox = lambda instance_id: DropboxDropbox(
        instance_id=instance_id, client=connections.client
    )
