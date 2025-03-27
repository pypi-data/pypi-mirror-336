"""Tests for SmartHub MCP extension."""
import os
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient

from smarthub_extension.config import Config
from smarthub_extension.server import app
from smarthub_extension.types import ConnectionResponse, TablesResponse, MerchantResponse

# Create test client
client = TestClient(app)

# Test configuration
@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    return Config(
        snowflake_user="test_user",
        snowflake_account="test_account",
        snowflake_role="test_role",
        snowflake_warehouse="test_warehouse",
        log_file="/tmp/test_smarthub_mcp.log",
        debug=True
    )

# Test connection response
@pytest.fixture
def mock_connection_response():
    """Create a mock successful connection response."""
    return ConnectionResponse(
        status="success",
        role="test_role",
        message=None
    )

# Test tables response
@pytest.fixture
def mock_tables_response():
    """Create a mock successful tables response."""
    return TablesResponse(
        status="success",
        tables=[{
            "name": "TEST_TABLE",
            "schema": "PUBLIC",
            "database": "APP_MERCH_GROWTH",
            "kind": "TABLE"
        }],
        message=None
    )

# Test merchant response
@pytest.fixture
def mock_merchant_response():
    """Create a mock successful merchant response."""
    return MerchantResponse(
        status="success",
        summary={
            "merchant_token": "TEST123",
            "business_id": "12345",
            "business_name": "Test Business",
            "current_am": "Test AM",
            "am_team": "Test Team",
            "is_current": True,
            "last_updated": "2025-03-25"
        },
        details={
            "ownership": {
                "merchant_token": "TEST123",
                "business_id": "12345",
                "active_owner_id": "OWNER123",
                "has_unexpired_dm": True,
                "time_start": "2025-01-01",
                "time_end": None,
                "is_current": True
            }
        },
        data_sources=["DIM_AM_OWNERSHIP_HISTORICAL"],
        message=None
    )

@pytest.mark.asyncio
async def test_test_snowflake_connection(mock_config):
    """Test the Snowflake connection test function."""
    with patch("smarthub_extension.server.get_snowflake_connection") as mock_get_conn:
        # Setup mock cursor
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = ["test_role"]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        
        response = client.post("/mcp/test_snowflake_connection")
        assert response.status_code == 200
        result = response.json()
        
        assert result["status"] == "success"
        assert result["role"] == "test_role"

@pytest.mark.asyncio
async def test_list_available_tables(mock_config):
    """Test the list available tables function."""
    with patch("smarthub_extension.server.get_snowflake_connection") as mock_get_conn:
        # Setup mock cursor
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            ["APP_MERCH_GROWTH", "TEST_TABLE", "PUBLIC", "TABLE"]
        ]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        
        response = client.post("/mcp/list_available_tables")
        assert response.status_code == 200
        result = response.json()
        
        assert result["status"] == "success"
        assert len(result["tables"]) == 1
        assert result["tables"][0]["name"] == "TEST_TABLE"

@pytest.mark.asyncio
async def test_get_merchant_info(mock_config):
    """Test the get merchant info function."""
    with patch("smarthub_extension.server.get_snowflake_connection") as mock_get_conn:
        # Setup mock cursor
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = [
            "TEST123", "12345", "OWNER123", True, "2025-01-01", None, True
        ]
        mock_cursor.description = [
            ("merchant_token", None), ("business_id", None),
            ("active_owner_id", None), ("has_unexpired_dm", None),
            ("time_start", None), ("time_end", None), ("is_current", None)
        ]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        
        response = client.post("/mcp/get_merchant_info/TEST123")
        assert response.status_code == 200
        result = response.json()
        
        assert result["status"] == "success"
        assert result["summary"]["merchant_token"] == "TEST123"
        assert "DIM_AM_OWNERSHIP_HISTORICAL" in result["data_sources"]