import inspect
import mcp
import mcp.server
import mcp.server.lowlevel

print("=== MCP Server Classes ===")
for name, obj in inspect.getmembers(mcp.server):
    if inspect.isclass(obj):
        print(f"\nClass: {name}")
        print("Methods:")
        for method_name, method in inspect.getmembers(obj, inspect.isfunction):
            if not method_name.startswith('_'):
                print(f"- {method_name}{inspect.signature(method)}")

print("\n=== MCP Server Lowlevel Classes ===")
for name, obj in inspect.getmembers(mcp.server.lowlevel):
    if inspect.isclass(obj):
        print(f"\nClass: {name}")
        print("Methods:")
        for method_name, method in inspect.getmembers(obj, inspect.isfunction):
            if not method_name.startswith('_'):
                print(f"- {method_name}{inspect.signature(method)}")

print("\n=== Full MCP Package Structure ===")
def print_module_tree(module, indent=0):
    print(" " * indent + module.__name__)
    for loader, name, is_pkg in pkgutil.iter_modules(module.__path__):
        full_name = module.__name__ + '.' + name
        spec = importlib.util.find_spec(full_name)
        if spec:
            new_module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(new_module)
                if is_pkg:
                    print_module_tree(new_module, indent + 2)
                else:
                    print(" " * (indent + 2) + name)
            except Exception as e:
                print(" " * (indent + 2) + f"{name} (error: {str(e)})")

import pkgutil
import importlib.util
print_module_tree(mcp)