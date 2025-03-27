# SmartHub MCP Extension

A natural language interface for SmartHub data and portfolio management.

## Features

- Natural language queries for merchant data
- Comprehensive merchant information lookup
- AM ownership and team data
- Business relationship mapping
- Integration with Goose AI assistant

## Installation

1. Clone the repository:
```bash
git clone git@github.com:squareup/smarthub-extension.git
cd smarthub-extension
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[test,dev]"
```

## Configuration

1. Set up environment variables:
```bash
export SNOWFLAKE_USER="your_username"
export SNOWFLAKE_ACCOUNT="your_account"
export SNOWFLAKE_ROLE="your_role"
export SNOWFLAKE_WAREHOUSE="your_warehouse"
```

2. Or create a configuration file:
```python
# config.py
config = {
    "snowflake_user": "your_username",
    "snowflake_account": "your_account",
    "snowflake_role": "your_role",
    "snowflake_warehouse": "your_warehouse",
    "log_file": "/path/to/log/file.log",
    "debug": False
}
```

## Example Queries

### Basic Merchant Lookup

```python
# Look up merchant by token
result = await get_merchant_info("MLM7X617NKATG")
print(f"Business Name: {result['summary']['business_name']}")
print(f"Current AM: {result['summary']['current_am']}")

# Look up merchant by business ID
result = await get_merchant_info("302718489")
print(f"Merchant Token: {result['summary']['merchant_token']}")
print(f"AM Team: {result['summary']['am_team']}")
```

### List Available Tables

```python
# Get all available tables
result = await list_available_tables()
for table in result["tables"]:
    print(f"Table: {table['name']} in {table['schema']}")
```

### Test Connection

```python
# Verify Snowflake connection
result = await test_snowflake_connection()
if result["status"] == "success":
    print(f"Connected as role: {result['role']}")
else:
    print(f"Connection failed: {result['message']}")
```

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=smarthub_extension

# Run specific test file
pytest tests/test_server.py -v

# Run tests and generate coverage report
pytest tests/ -v --cov=smarthub_extension --cov-report=html
```

### Code Quality

```bash
# Run linter
ruff check .

# Run type checker
mypy smarthub_extension

# Format code
black .
```

### Creating a Release

1. Update version in `pyproject.toml`
2. Create and push a tag:
```bash
git tag -a v0.1.2 -m "Release version 0.1.2"
git push origin v0.1.2
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details