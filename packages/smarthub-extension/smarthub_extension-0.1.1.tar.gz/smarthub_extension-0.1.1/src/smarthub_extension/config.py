from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Settings for the SmartHub MCP extension."""
    snowflake_account: str
    snowflake_user: str
    snowflake_password: str
    snowflake_warehouse: str
    snowflake_role: str
    snowflake_database: str = "APP_MERCH_GROWTH"

    class Config:
        env_file = ".env"
        env_prefix = "SNOWFLAKE_"