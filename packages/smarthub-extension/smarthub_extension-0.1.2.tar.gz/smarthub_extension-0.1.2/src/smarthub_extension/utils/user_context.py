"""User context management for SmartHub queries"""
import os
import snowflake.connector

class UserContext:
    def __init__(self):
        self._current_user = None
    
    async def get_current_user(self) -> str:
        """Get the current user's email from Snowflake connection"""
        if self._current_user is None:
            try:
                conn = snowflake.connector.connect(
                    user=os.getenv('USER', 'unknown') + '@squareup.com',
                    account='square',
                    authenticator='externalbrowser'
                )
                cur = conn.cursor()
                cur.execute('SELECT CURRENT_USER()')
                self._current_user = cur.fetchone()[0]
                cur.close()
                conn.close()
            except Exception as e:
                raise Exception(f"Failed to get current user: {str(e)}")
        
        return self._current_user