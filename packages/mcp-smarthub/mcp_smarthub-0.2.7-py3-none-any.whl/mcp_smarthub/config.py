"""Configuration management for SmartHub extension."""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """SmartHub extension configuration."""
    snowflake_user: str = os.getenv("SNOWFLAKE_USER", "")
    snowflake_account: str = os.getenv("SNOWFLAKE_ACCOUNT", "square")
    snowflake_role: str = os.getenv("SNOWFLAKE_ROLE", "ANALYST_MERCH_GROWTH")
    snowflake_warehouse: str = os.getenv("SNOWFLAKE_WAREHOUSE", "ANALYST_WH")
    log_file: str = os.getenv("SMARTHUB_LOG_FILE", "/tmp/smarthub_mcp.log")
    debug: bool = os.getenv("SMARTHUB_DEBUG", "").lower() == "true"

    @property
    def is_valid(self) -> bool:
        """Check if configuration is valid."""
        return bool(self.snowflake_user)

    def validate(self) -> Optional[str]:
        """Validate configuration and return error message if invalid."""
        if not self.snowflake_user:
            return "SNOWFLAKE_USER environment variable is required"
        return None

# Global config instance
config = Config()