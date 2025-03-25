from typing import Any
from .api import DocusignDocusign  # type: ignore
from .models import *  # type: ignore


def register_connector(connections: Any):
    """Register the docusign_docusign connector."""
    connections.docusign_docusign = lambda instance_id: DocusignDocusign(
        instance_id=instance_id, client=connections.client
    )
