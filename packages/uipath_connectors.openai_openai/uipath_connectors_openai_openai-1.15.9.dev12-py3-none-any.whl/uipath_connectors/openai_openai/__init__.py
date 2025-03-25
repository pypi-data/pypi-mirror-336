from typing import Any
from .api import OpenaiOpenai  # type: ignore
from .models import *  # type: ignore


def register_connector(connections: Any):
    """Register the openai_openai connector."""
    connections.openai_openai = lambda instance_id: OpenaiOpenai(
        instance_id=instance_id, client=connections.client
    )
