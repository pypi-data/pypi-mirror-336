#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from smarthub_extension.server import mcp

if __name__ == "__main__":
    mcp.run(transport='stdio')