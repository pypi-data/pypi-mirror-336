"""Snowflake utility functions for SmartHub extension."""
import os
from datetime import datetime
from typing import Any

import snowflake.connector
from snowflake.connector import SnowflakeConnection

from ..config import config

def log_to_file(message: str) -> None:
    """Write a log message to the configured log file.
    
    Args:
        message: The message to log
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    
    try:
        with open(config.log_file, "a") as f:
            f.write(log_message)
    except Exception as e:
        print(f"Failed to write to log file: {e}")
        print(log_message)

def get_snowflake_connection() -> SnowflakeConnection:
    """Get a connection to Snowflake using configured credentials.
    
    Returns:
        SnowflakeConnection: An authenticated Snowflake connection
    
    Raises:
        ValueError: If required configuration is missing
        Exception: If connection fails
    """
    if error := config.validate():
        raise ValueError(error)
        
    try:
        return snowflake.connector.connect(
            user=config.snowflake_user,
            account=config.snowflake_account,
            authenticator="externalbrowser",
            role=config.snowflake_role,
            warehouse=config.snowflake_warehouse
        )
    except Exception as e:
        log_to_file(f"Failed to connect to Snowflake: {str(e)}")
        raise