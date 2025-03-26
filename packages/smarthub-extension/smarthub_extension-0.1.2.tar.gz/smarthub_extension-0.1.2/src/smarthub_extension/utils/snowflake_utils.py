"""Snowflake utilities for SmartHub extension"""
import os
import logging
import snowflake.connector
from snowflake.connector.connection import SnowflakeConnection

def log_to_file(message: str) -> None:
    """Log message to file"""
    log_file = os.getenv("SMARTHUB_LOG_FILE", "/tmp/smarthub_mcp.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info(message)

def get_snowflake_connection() -> SnowflakeConnection:
    """Get Snowflake connection with proper role and warehouse"""
    try:
        # Connect with APP_MERCH_GROWTH role
        conn = snowflake.connector.connect(
            account='square',
            user=os.getenv('SNOWFLAKE_USER', 'mbrown@squareup.com'),
            authenticator='externalbrowser',
            role='APP_MERCH_GROWTH__SNOWFLAKE__READ_ONLY',
            warehouse='ADHOC__MEDIUM',
            database='APP_MERCH_GROWTH',
            schema='PUBLIC',
            browser_response_timeout=120
        )
        return conn
        
    except Exception as e:
        log_to_file(f"Failed to connect to Snowflake: {str(e)}")
        raise