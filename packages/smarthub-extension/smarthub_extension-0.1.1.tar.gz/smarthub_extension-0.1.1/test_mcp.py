import mcp
import pkgutil

print("MCP version:", getattr(mcp, '__version__', 'unknown'))
print("\nMCP contents:")
for item in dir(mcp):
    if not item.startswith('_'):
        print(f"- {item}")

print("\nMCP submodules:")
for module in pkgutil.iter_modules(mcp.__path__):
    print(f"- {module.name}")

print("\nAvailable from mcp.server:")
import mcp.server
for item in dir(mcp.server):
    if not item.startswith('_'):
        print(f"- {item}")