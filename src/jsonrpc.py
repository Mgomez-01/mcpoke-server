"""
JSON-RPC 2.0 implementation for the MCP protocol.

This module handles the JSON-RPC 2.0 message formatting and processing
as required by the Model Context Protocol (MCP).
"""

import json
import uuid
from typing import Any, Dict, List, Optional, Union

# JSON-RPC 2.0 error codes
ERROR_PARSE_ERROR = -32700
ERROR_INVALID_REQUEST = -32600
ERROR_METHOD_NOT_FOUND = -32601
ERROR_INVALID_PARAMS = -32602
ERROR_INTERNAL_ERROR = -32603
ERROR_SERVER_ERROR_START = -32000
ERROR_SERVER_ERROR_END = -32099

class JsonRpcError(Exception):
    """JSON-RPC 2.0 error."""
    
    def __init__(self, code: int, message: str, data: Any = None):
        """
        Initialize a JSON-RPC error.
        
        Args:
            code: Error code
            message: Error message
            data: Additional error data
        """
        self.code = code
        self.message = message
        self.data = data
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the error to a dictionary.
        
        Returns:
            Error dictionary
        """
        error = {
            "code": self.code,
            "message": self.message
        }
        
        if self.data is not None:
            error["data"] = self.data
        
        return error

class JsonRpcRequest:
    """JSON-RPC 2.0 request."""
    
    def __init__(
        self,
        method: str,
        params: Optional[Union[List[Any], Dict[str, Any]]] = None,
        request_id: Optional[Union[str, int]] = None,
        jsonrpc: str = "2.0"
    ):
        """
        Initialize a JSON-RPC request.
        
        Args:
            method: Method to call
            params: Method parameters
            request_id: Request ID (None for notifications)
            jsonrpc: JSON-RPC version
        """
        self.jsonrpc = jsonrpc
        self.method = method
        self.params = params
        self.id = request_id
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JsonRpcRequest':
        """
        Create a request from a dictionary.
        
        Args:
            data: Request dictionary
        
        Returns:
            JsonRpcRequest instance
        
        Raises:
            JsonRpcError: If the request is invalid
        """
        if not isinstance(data, dict):
            raise JsonRpcError(
                ERROR_INVALID_REQUEST,
                "Invalid request: not an object"
            )
        
        if data.get("jsonrpc") != "2.0":
            raise JsonRpcError(
                ERROR_INVALID_REQUEST,
                "Invalid request: invalid jsonrpc version"
            )
        
        if "method" not in data:
            raise JsonRpcError(
                ERROR_INVALID_REQUEST,
                "Invalid request: method not specified"
            )
        
        if not isinstance(data["method"], str):
            raise JsonRpcError(
                ERROR_INVALID_REQUEST,
                "Invalid request: method must be a string"
            )
        
        params = data.get("params")
        if params is not None and not isinstance(params, (list, dict)):
            raise JsonRpcError(
                ERROR_INVALID_REQUEST,
                "Invalid request: params must be an array or object"
            )
        
        return cls(
            method=data["method"],
            params=params,
            request_id=data.get("id"),
            jsonrpc=data["jsonrpc"]
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the request to a dictionary.
        
        Returns:
            Request dictionary
        """
        request = {
            "jsonrpc": self.jsonrpc,
            "method": self.method
        }
        
        if self.params is not None:
            request["params"] = self.params
        
        if self.id is not None:
            request["id"] = self.id
        
        return request
    
    def to_json(self) -> str:
        """
        Convert the request to a JSON string.
        
        Returns:
            JSON string
        """
        return json.dumps(self.to_dict())
    
    def is_notification(self) -> bool:
        """
        Check if the request is a notification.
        
        Returns:
            True if the request is a notification, False otherwise
        """
        return self.id is None

class JsonRpcResponse:
    """JSON-RPC 2.0 response."""
    
    def __init__(
        self,
        result: Any = None,
        error: Optional[Dict[str, Any]] = None,
        response_id: Optional[Union[str, int]] = None,
        jsonrpc: str = "2.0"
    ):
        """
        Initialize a JSON-RPC response.
        
        Args:
            result: Result of the method call
            error: Error information
            response_id: Response ID
            jsonrpc: JSON-RPC version
        """
        self.jsonrpc = jsonrpc
        self.result = result
        self.error = error
        self.id = response_id
    
    @classmethod
    def success(
        cls,
        result: Any,
        response_id: Optional[Union[str, int]] = None
    ) -> 'JsonRpcResponse':
        """
        Create a success response.
        
        Args:
            result: Result of the method call
            response_id: Response ID
        
        Returns:
            JsonRpcResponse instance
        """
        return cls(result=result, response_id=response_id)
    
    @classmethod
    def error(
        cls,
        error: JsonRpcError,
        response_id: Optional[Union[str, int]] = None
    ) -> 'JsonRpcResponse':
        """
        Create an error response.
        
        Args:
            error: Error information
            response_id: Response ID
        
        Returns:
            JsonRpcResponse instance
        """
        return cls(error=error.to_dict(), response_id=response_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the response to a dictionary.
        
        Returns:
            Response dictionary
        """
        response = {
            "jsonrpc": self.jsonrpc,
            "id": self.id
        }
        
        if self.error is not None:
            response["error"] = self.error
        else:
            response["result"] = self.result
        
        return response
    
    def to_json(self) -> str:
        """
        Convert the response to a JSON string.
        
        Returns:
            JSON string
        """
        return json.dumps(self.to_dict())

def generate_id() -> str:
    """
    Generate a unique request ID.
    
    Returns:
        Unique ID
    """
    return str(uuid.uuid4())
