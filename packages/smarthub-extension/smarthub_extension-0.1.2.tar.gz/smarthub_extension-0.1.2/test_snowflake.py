import snowflake.connector
import os

print("Testing Snowflake connection...")

# Connection settings
settings = {
    'user': 'mbrown@squareup.com',
    'account': 'square',
    'authenticator': 'externalbrowser',
    'role': 'MBROWN',
    'warehouse': 'ADHOC__MEDIUM',
    'database': 'APP_MERCH_GROWTH',
    'schema': 'PUBLIC'
}

print("\nConnection settings:")
for key, value in settings.items():
    print(f"{key} = {value}")

print("\nTrying to connect...")
try:
    conn = snowflake.connector.connect(**settings)
    print("Connected!")
    
    cur = conn.cursor()
    print("Executing test query...")
    
    cur.execute("SELECT current_user(), current_role(), current_warehouse()")
    result = cur.fetchone()
    print(f"User: {result[0]}")
    print(f"Role: {result[1]}")
    print(f"Warehouse: {result[2]}")
    
    cur.close()
    conn.close()
    print("\nSuccess!")
    
except Exception as e:
    print(f"\nError: {type(e)}: {str(e)}")
    print("Error details:", str(e.__dict__))