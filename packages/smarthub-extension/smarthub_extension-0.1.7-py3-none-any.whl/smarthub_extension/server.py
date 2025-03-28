"""SmartHub MCP Server - Main server implementation."""
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from mcp.server import FastMCP

from .config import config
from .types import (
    ConnectionResponse,
    TablesResponse,
    MerchantResponse,
    TableInfo,
    MerchantSummary
)
from .utils.snowflake_utils import get_snowflake_connection, log_to_file

# Initialize FastAPI app
app = FastAPI(
    title="SmartHub MCP",
    description="SmartHub data access extension for Goose",
    version="0.1.6"
)

# Initialize MCP server
mcp = FastMCP(name="smarthub")

# Define core functionality
async def _test_snowflake_connection() -> ConnectionResponse:
    """Test if we can connect to and query the SmartHub Snowflake tables."""
    log_to_file("\n=== Testing Snowflake Connection ===")
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT current_role()")
        role = cur.fetchone()[0]
        
        return ConnectionResponse(
            status="success",
            role=str(role),
            message=None
        )
        
    except Exception as e:
        log_to_file(f"Connection test failed: {str(e)}")
        return ConnectionResponse(
            status="error",
            role=None,
            message=str(e)
        )

async def _list_available_tables() -> TablesResponse:
    """List all tables available in the APP_MERCH_GROWTH database."""
    log_to_file("Listing available tables...")
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        # Get table info
        cur.execute("""
            SHOW TABLES IN DATABASE APP_MERCH_GROWTH;
        """)
        tables = cur.fetchall()
        
        # Format table info
        table_info = [TableInfo(
            name=str(row[1]),
            schema=str(row[2]),
            database=str(row[0]),
            kind=str(row[3])
        ) for row in tables]
        
        return TablesResponse(
            status="success",
            tables=table_info,
            message=None
        )
        
    except Exception as e:
        log_to_file(f"Failed to list tables: {str(e)}")
        return TablesResponse(
            status="error",
            tables=None,
            message=str(e)
        )

async def _get_merchant_info(merchant_token: str) -> MerchantResponse:
    """Get comprehensive information about a merchant using their token or business ID."""
    log_to_file(f"Fetching merchant info for token/id: {merchant_token}")
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()
        
        # First, let's try to find the merchant in any available tables
        merchant_data: Dict[str, Any] = {}
        data_sources = []
        
        # Convert input to string if it's not already
        merchant_token = str(merchant_token)
        
        # Check if input is numeric (business ID)
        is_business_id = merchant_token.replace("-", "").isdigit()
        log_to_file(f"Input appears to be a {'business ID' if is_business_id else 'merchant token'}")
        
        # First check DIM_AM_OWNERSHIP_HISTORICAL
        if not is_business_id:
            cur.execute("""
                SELECT 
                    MERCHANT_TOKEN,
                    BUSINESS_ID,
                    ACTIVE_OWNER_ID,
                    HAS_UNEXPIRED_DM,
                    TIME_START,
                    TIME_END,
                    IS_CURRENT
                FROM APP_MERCH_GROWTH.PUBLIC.DIM_AM_OWNERSHIP_HISTORICAL
                WHERE MERCHANT_TOKEN = %s
                AND IS_CURRENT = TRUE
                ORDER BY TIME_START DESC
                LIMIT 1
            """, (merchant_token,))
            
            result = cur.fetchone()
            if result:
                column_names = [desc[0].lower() for desc in cur.description]
                ownership_data = dict(zip(column_names, [str(val) if val is not None else None for val in result]))
                merchant_data["ownership"] = ownership_data
                data_sources.append("DIM_AM_OWNERSHIP_HISTORICAL")
                
                # If we found a business_id, store it for later
                if ownership_data.get("business_id"):
                    merchant_token = ownership_data["business_id"]
                    is_business_id = True
        
        # Check ITD_RUN_MERCHANTS_COMBINED_AM_TEAM
        if not is_business_id:
            cur.execute("""
                SELECT 
                    MERCHANT_TOKEN,
                    TREATMENT_GROUP,
                    AM_TEAM,
                    PREFERRED_NAME as AM_NAME,
                    SFDC_OWNER_ID,
                    TREATMENT_MONTH,
                    TREATMENT_QUARTER
                FROM APP_MERCH_GROWTH.PUBLIC.ITD_RUN_MERCHANTS_COMBINED_AM_TEAM
                WHERE MERCHANT_TOKEN = %s
                ORDER BY TREATMENT_MONTH DESC
                LIMIT 1
            """, (merchant_token,))
            
            result = cur.fetchone()
            if result:
                column_names = [desc[0].lower() for desc in cur.description]
                am_data = dict(zip(column_names, [str(val) if val is not None else None for val in result]))
                merchant_data["am_info"] = am_data
                data_sources.append("ITD_RUN_MERCHANTS_COMBINED_AM_TEAM")
        
        # Check PAYOUT_TOOL_BUSINESS_ID_MAP_EXAMPLE
        query = """
            SELECT 
                BUSINESS_ID,
                BUSINESS_NAME,
                MERCHANT_CLUSTER_NAME,
                USER_TOKEN,
                ULTIMATE_PARENT_ACCOUNT_ID,
                ACCOUNT_ID,
                IS_ULTIMATE_PARENT
            FROM APP_MERCH_GROWTH.PUBLIC.PAYOUT_TOOL_BUSINESS_ID_MAP_EXAMPLE
            WHERE {column} = '{value}'
        """.format(
            column="BUSINESS_ID" if is_business_id else "USER_TOKEN",
            value=merchant_token
        )
        
        cur.execute(query)
        result = cur.fetchone()
        if result:
            column_names = [desc[0].lower() for desc in cur.description]
            business_data = dict(zip(column_names, [str(val) if val is not None else None for val in result]))
            merchant_data["business"] = business_data
            data_sources.append("PAYOUT_TOOL_BUSINESS_ID_MAP_EXAMPLE")
            
            # If we found data by business_id, also check for AM info using the user_token
            if is_business_id and business_data.get("user_token") and "am_info" not in merchant_data:
                cur.execute("""
                    SELECT 
                        MERCHANT_TOKEN,
                        TREATMENT_GROUP,
                        AM_TEAM,
                        PREFERRED_NAME as AM_NAME,
                        SFDC_OWNER_ID,
                        TREATMENT_MONTH,
                        TREATMENT_QUARTER
                    FROM APP_MERCH_GROWTH.PUBLIC.ITD_RUN_MERCHANTS_COMBINED_AM_TEAM
                    WHERE MERCHANT_TOKEN = %s
                    ORDER BY TREATMENT_MONTH DESC
                    LIMIT 1
                """, (business_data["user_token"],))
                
                result = cur.fetchone()
                if result:
                    column_names = [desc[0].lower() for desc in cur.description]
                    am_data = dict(zip(column_names, [str(val) if val is not None else None for val in result]))
                    merchant_data["am_info"] = am_data
                    if "ITD_RUN_MERCHANTS_COMBINED_AM_TEAM" not in data_sources:
                        data_sources.append("ITD_RUN_MERCHANTS_COMBINED_AM_TEAM")
        
        if merchant_data:
            # Add summary section
            summary = MerchantSummary(
                merchant_token=merchant_data.get("ownership", {}).get("merchant_token") or 
                              merchant_data.get("am_info", {}).get("merchant_token") or 
                              merchant_data.get("business", {}).get("user_token"),
                business_id=merchant_data.get("ownership", {}).get("business_id") or 
                           merchant_data.get("business", {}).get("business_id"),
                business_name=merchant_data.get("business", {}).get("business_name"),
                current_am=merchant_data.get("am_info", {}).get("am_name"),
                am_team=merchant_data.get("am_info", {}).get("am_team"),
                is_current=merchant_data.get("ownership", {}).get("is_current"),
                last_updated=merchant_data.get("am_info", {}).get("treatment_month")
            )
            
            return MerchantResponse(
                status="success",
                summary=summary,
                details=merchant_data,
                data_sources=data_sources,
                message=None
            )
        
        return MerchantResponse(
            status="error",
            summary=None,
            details=None,
            data_sources=[],
            message=f"No data found for {'business ID' if is_business_id else 'merchant token'}: {merchant_token}"
        )
        
    except Exception as e:
        log_to_file(f"Failed to get merchant info: {str(e)}")
        return MerchantResponse(
            status="error",
            summary=None,
            details=None,
            data_sources=[],
            message=str(e)
        )

# Register MCP tools
@mcp.tool()
async def test_snowflake_connection() -> ConnectionResponse:
    """Test if we can connect to and query the SmartHub Snowflake tables."""
    return await _test_snowflake_connection()

@mcp.tool()
async def list_available_tables() -> TablesResponse:
    """List all tables available in the APP_MERCH_GROWTH database."""
    return await _list_available_tables()

@mcp.tool()
async def get_merchant_info(merchant_token: str) -> MerchantResponse:
    """Get comprehensive information about a merchant using their token or business ID."""
    return await _get_merchant_info(merchant_token)

@app.on_event("startup")
async def startup_event() -> None:
    """Validate configuration on startup."""
    if error := config.validate():
        raise HTTPException(status_code=500, detail=error)
    log_to_file("SmartHub MCP Server starting up...")

def run_server() -> None:
    """Run the MCP server."""
    mcp.run()