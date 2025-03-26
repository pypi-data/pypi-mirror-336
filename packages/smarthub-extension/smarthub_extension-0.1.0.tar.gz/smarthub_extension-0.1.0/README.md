# SmartHub MCP Extension

A Goose extension for accessing SmartHub data through Snowflake.

## Installation

```bash
pip install smarthub-extension
```

## Usage

### With Goose

Add to your Goose configuration:

```yaml
extensions:
  smarthub:
    type: stdio
    command: smarthub run --transport stdio
    environment:
      PYTHONPATH: /path/to/smarthub_extension
      SMARTHUB_LOG_FILE: /tmp/smarthub_mcp.log
```

### Standalone Server

Run as a standalone server:

```bash
smarthub run --transport http --host 127.0.0.1 --port 8000
```

## Features

- Query merchant information by token or business ID
- Access AM ownership data
- View business relationships and hierarchies
- Track merchant history and status

## Development

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -e .
   ```
4. Run tests:
   ```bash
   pytest
   ```

## License

MIT