from typing import Any
from .api import SnowflakeSnowflake  # type: ignore
from .models import *  # type: ignore


def register_connector(connections: Any):
    """Register the snowflake_snowflake connector."""
    connections.snowflake_snowflake = lambda instance_id: SnowflakeSnowflake(
        instance_id=instance_id, client=connections.client
    )
