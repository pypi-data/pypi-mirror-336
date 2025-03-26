"""CLI entry point for SmartHub MCP extension"""
import typer
import uvicorn
from ..server import app, mcp

cli = typer.Typer()

@cli.command()
def run(
    transport: str = "stdio",
    host: str = "127.0.0.1",
    port: int = 8000,
):
    """Run the SmartHub MCP extension server"""
    if transport == "stdio":
        # Run in stdio mode (for Goose)
        mcp.run()
    else:
        # Run as FastAPI server
        uvicorn.run(app, host=host, port=port)