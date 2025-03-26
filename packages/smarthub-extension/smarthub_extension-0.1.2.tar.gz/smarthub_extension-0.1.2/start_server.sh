#!/bin/bash

# Create Snowflake config directory
mkdir -p ~/.snowflake

# Create Snowflake config file
cat > ~/.snowflake/config << EOF
[connections]
authenticator = externalbrowser
accountname = square
username = mbrown@squareup.com
rolename = MBROWN
warehousename = ADHOC__MEDIUM
dbname = APP_MERCH_GROWTH
schemaname = PUBLIC
EOF

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment and start the server
source venv/bin/activate
PYTHONPATH=$PYTHONPATH:$(pwd) python -m src.smarthub_extension.server