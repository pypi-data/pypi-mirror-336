"""Common type definitions for SmartHub extension"""
from typing import Dict, List, Any, Optional, Union

# Type aliases
JSONDict = Dict[str, Any]
QueryResult = Dict[str, Any]
Parameters = Dict[str, Any]

# Common return types
class ResponseStatus:
    SUCCESS = "success"
    ERROR = "error"
    NEEDS_CLARIFICATION = "needs_clarification"