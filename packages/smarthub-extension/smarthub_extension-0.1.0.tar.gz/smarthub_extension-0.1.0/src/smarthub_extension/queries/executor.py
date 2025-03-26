"""Query executor for SmartHub data"""
from typing import Dict, Any, List, Optional
from snowflake.connector.connection import SnowflakeConnection
from ..utils.snowflake_utils import get_snowflake_connection, log_to_file

class QueryExecutor:
    def __init__(self):
        self.conn = None
    
    def _get_connection(self) -> SnowflakeConnection:
        """Get or create Snowflake connection"""
        if not self.conn:
            self.conn = get_snowflake_connection()
        return self.conn
    
    async def execute_query(self, intent: str, parameters: Dict[str, Any], am_email: str) -> Dict[str, Any]:
        """Execute appropriate query based on intent"""
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            
            if intent == "test_connection":
                cur.execute("""
                    SELECT 
                        current_user() as username,
                        current_role() as role,
                        current_warehouse() as warehouse
                """)
                result = cur.fetchone()
                username, role, warehouse = result
                return {
                    "status": "success",
                    "connection_info": {
                        "username": str(username),
                        "role": str(role),
                        "warehouse": str(warehouse)
                    }
                }
                
            elif intent == "list_tables":
                # Use SHOW TABLES instead of INFORMATION_SCHEMA
                cur.execute("SHOW TABLES")
                results = cur.fetchall()
                return {
                    "status": "success",
                    "tables": [str(row[1]) for row in results]
                }
                
            elif intent == "get_merchant_info":
                merchant_token = parameters.get("merchant_token")
                if not merchant_token:
                    return {"status": "error", "message": "Missing merchant token"}
                    
                # Try different tables/views that might have merchant info
                tables_to_try = [
                    "MERCHANT_SUMMARY",
                    "MERCHANT_PROFILE",
                    "MERCHANT_DATA"
                ]
                
                for table in tables_to_try:
                    try:
                        query = f"""
                            SELECT *
                            FROM {table}
                            WHERE merchant_token = %s
                            LIMIT 1
                        """
                        cur.execute(query, (merchant_token,))
                        result = cur.fetchone()
                        if result:
                            column_names = [desc[0] for desc in cur.description]
                            return {
                                "status": "success",
                                "data": {
                                    name: str(value) for name, value in zip(column_names, result)
                                }
                            }
                    except Exception as e:
                        log_to_file(f"Failed to query {table}: {str(e)}")
                        continue
                
                return {
                    "status": "error",
                    "message": "Merchant not found or no access to merchant data"
                }
            
            else:
                return {
                    "status": "error",
                    "message": f"Unknown intent: {intent}"
                }
                
        except Exception as e:
            log_to_file(f"Query execution failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
        finally:
            if cur:
                cur.close()