"""CLI entry point for SmartHub MCP extension"""
import typer
import uvicorn
from fastapi import FastAPI
from mcp.server import FastMCP

from smarthub_extension.server import mcp

app = FastAPI()
cli = typer.Typer()

@cli.command()
def run(
    host: str = "127.0.0.1",
    port: int = 8000,
    transport: str = "stdio"
):
    """Run the SmartHub MCP extension server"""
    if transport == "stdio":
        # Run in stdio mode (for Goose)
        mcp.run(transport="stdio")
    else:
        # Run as FastAPI server
        app.mount("/mcp", mcp.app)
        uvicorn.run(app, host=host, port=port)