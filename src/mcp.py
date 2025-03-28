"""
Model Context Protocol (MCP) implementation.

This module implements the MCP protocol lifecycle and handling.
"""

import json
import logging
import sys
from typing import Any, Callable, Dict, List, Optional, Union, cast

from .jsonrpc import (
    JsonRpcError,
    JsonRpcRequest,
    JsonRpcResponse,
    generate_id,
    ERROR_METHOD_NOT_FOUND,
    ERROR_INVALID_PARAMS,
    ERROR_INTERNAL_ERROR
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcpoke-mcp')

class McpCapability:
    """MCP capability definition."""
    
    def __init__(self, name: str, version: str, features: Optional[List[str]] = None):
        """
        Initialize an MCP capability.
        
        Args:
            name: Capability name
            version: Capability version
            features: Capability features
        """
        self.name = name
        self.version = version
        self.features = features or []
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the capability to a dictionary.
        
        Returns:
            Capability dictionary
        """
        result = {
            "name": self.name,
            "version": self.version
        }
        
        if self.features:
            result["features"] = self.features
        
        return result

class McpTool:
    """MCP tool definition."""
    
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Callable[[Dict[str, Any]], Any]
    ):
        """
        Initialize an MCP tool.
        
        Args:
            name: Tool name
            description: Tool description
            parameters: Tool parameters schema
            handler: Tool handler function
        """
        self.name = name
        self.description = description
        self.parameters = parameters
        self.handler = handler
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tool to a dictionary.
        
        Returns:
            Tool dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

class McpSession:
    """MCP session state."""
    
    def __init__(self):
        """Initialize an MCP session."""
        self.initialized = False
        self.client_capabilities: Dict[str, Dict[str, Any]] = {}
        self.negotiated_capabilities: Dict[str, Dict[str, Any]] = {}
        self.context: Dict[str, Any] = {}

class McpProtocolHandler:
    """MCP protocol handler."""
    
    def __init__(self, server_instance: Any):
        """
        Initialize an MCP protocol handler.
        
        Args:
            server_instance: Server instance
        """
        self.server = server_instance
        self.tools: Dict[str, McpTool] = {}
        self.capabilities: Dict[str, McpCapability] = {}
        self.sessions: Dict[str, McpSession] = {}
        
        # Register core capabilities
        self.register_capability(McpCapability(
            name="core",
            version="1.0",
            features=["initialize", "shutdown"]
        ))
        
        # Register tools capability
        self.register_capability(McpCapability(
            name="tools",
            version="1.0",
            features=[]
        ))
        
        # Register core methods
        self.register_method("initialize", self._handle_initialize)
        self.register_method("shutdown", self._handle_shutdown)
        self.register_method("listTools", self._handle_list_tools)
        self.register_method("invokeTools.pokemon", self._handle_pokemon_tool)
    
    def register_capability(self, capability: McpCapability):
        """
        Register an MCP capability.
        
        Args:
            capability: Capability to register
        """
        self.capabilities[capability.name] = capability
    
    def register_tool(self, tool: McpTool):
        """
        Register an MCP tool.
        
        Args:
            tool: Tool to register
        """
        self.tools[tool.name] = tool
        # Add tool to tools capability features
        if "tools" in self.capabilities:
            capability = self.capabilities["tools"]
            if tool.name not in capability.features:
                capability.features.append(tool.name)
    
    def register_method(self, method: str, handler: Callable[[Dict[str, Any], str], Any]):
        """
        Register an MCP method.
        
        Args:
            method: Method name
            handler: Method handler
        """
        setattr(self, f"_handle_{method.replace('.', '_')}", handler)
    
    def get_session(self, session_id: str) -> McpSession:
        """
        Get an MCP session.
        
        Args:
            session_id: Session ID
        
        Returns:
            MCP session
        """
        if session_id not in self.sessions:
            logger.debug(f"Creating new session: {session_id}")
            self.sessions[session_id] = McpSession()
        else:
            logger.debug(f"Using existing session: {session_id}")
            
        return self.sessions[session_id]
    
    def handle_request(self, data: Union[str, Dict[str, Any]], session_id: str = "") -> Optional[str]:
        """
        Handle an MCP request.
        
        Args:
            data: Request data
            session_id: Session ID
        
        Returns:
            Response data or None
        """
        try:
            # Parse request
            if isinstance(data, str):
                try:
                    request_data = json.loads(data)
                except json.JSONDecodeError:
                    response = JsonRpcResponse.error(
                        JsonRpcError(
                            -32700,
                            "Parse error"
                        ),
                        None
                    )
                    return response.to_json()
            else:
                request_data = data
            
            # Handle batch requests
            if isinstance(request_data, list):
                responses = []
                
                for item in request_data:
                    # Extract session ID from params if present
                    if isinstance(item, dict) and "params" in item and isinstance(item["params"], dict):
                        if "session_id" in item["params"]:
                            session_id = item["params"]["session_id"]
                    
                    result = self._handle_single_request(item, session_id)
                    if result is not None:
                        responses.append(result)
                
                if not responses:
                    return None
                
                return json.dumps(responses)
            else:
                # Extract session ID from params if present
                if isinstance(request_data, dict) and "params" in request_data and isinstance(request_data["params"], dict):
                    if "session_id" in request_data["params"]:
                        session_id = request_data["params"]["session_id"]
                
                response = self._handle_single_request(request_data, session_id)
                if response is not None:
                    return json.dumps(response)
                
                return None
        except Exception as e:
            logger.exception(f"Error handling request: {e}")
            response = JsonRpcResponse.error(
                JsonRpcError(
                    ERROR_INTERNAL_ERROR,
                    f"Internal error: {str(e)}"
                ),
                None
            )
            return response.to_json()
    
    def _handle_single_request(self, request_data: Dict[str, Any], session_id: str) -> Optional[Dict[str, Any]]:
        """
        Handle a single MCP request.
        
        Args:
            request_data: Request data
            session_id: Session ID
        
        Returns:
            Response data or None
        """
        try:
            # Parse request
            request = JsonRpcRequest.from_dict(request_data)
            
            # Skip session check for initialization and shutdown
            if request.method not in ["initialize", "shutdown"]:
                # Check if session is initialized
                session = self.get_session(session_id)
                if not session.initialized:
                    # Special case for HTTP - auto-initialize if needed
                    if session_id.startswith("http-") and request.method != "initialize":
                        logger.debug(f"Auto-initializing HTTP session: {session_id}")
                        # Auto-initialize the session with default capabilities
                        self._handle_initialize({
                            "capabilities": {
                                "core": {"version": "1.0"},
                                "tools": {"version": "1.0"}
                            }
                        }, session_id)
            
            # Check if method exists
            method_handler = getattr(self, f"_handle_{request.method.replace('.', '_')}", None)
            if method_handler is None:
                if request.is_notification():
                    return None
                
                response = JsonRpcResponse.error(
                    JsonRpcError(
                        ERROR_METHOD_NOT_FOUND,
                        f"Method not found: {request.method}"
                    ),
                    request.id
                )
                return response.to_dict()
            
            # Handle method
            try:
                params = request.params or {}
                # Remove session_id from params if present to avoid duplication
                if isinstance(params, dict) and "session_id" in params:
                    params = {k: v for k, v in params.items() if k != "session_id"}
                
                if isinstance(params, list):
                    result = method_handler(*params, session_id=session_id)
                else:
                    result = method_handler(params, session_id=session_id)
                
                if request.is_notification():
                    return None
                
                response = JsonRpcResponse.success(result, request.id)
                return response.to_dict()
            except TypeError as e:
                if request.is_notification():
                    return None
                
                response = JsonRpcResponse.error(
                    JsonRpcError(
                        ERROR_INVALID_PARAMS,
                        f"Invalid parameters: {str(e)}"
                    ),
                    request.id
                )
                return response.to_dict()
            except Exception as e:
                if request.is_notification():
                    return None
                
                response = JsonRpcResponse.error(
                    JsonRpcError(
                        ERROR_INTERNAL_ERROR,
                        f"Internal error: {str(e)}"
                    ),
                    request.id
                )
                return response.to_dict()
        except JsonRpcError as e:
            request_id = request_data.get("id") if isinstance(request_data, dict) else None
            
            if request_id is None:
                return None
            
            response = JsonRpcResponse.error(e, request_id)
            return response.to_dict()
        except Exception as e:
            logger.exception(f"Error handling request: {e}")
            
            request_id = request_data.get("id") if isinstance(request_data, dict) else None
            if request_id is None:
                return None
            
            response = JsonRpcResponse.error(
                JsonRpcError(
                    ERROR_INTERNAL_ERROR,
                    f"Internal error: {str(e)}"
                ),
                request_id
            )
            return response.to_dict()
    
    def _handle_initialize(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Handle the initialize method.
        
        Args:
            params: Method parameters
            session_id: Session ID
        
        Returns:
            Method result
        """
        logger.debug(f"Initializing session: {session_id}")
        session = self.get_session(session_id)
        
        # Store client capabilities
        session.client_capabilities = params.get("capabilities", {})
        
        # Negotiate capabilities
        negotiated_capabilities = {}
        
        for name, capability in self.capabilities.items():
            if name in session.client_capabilities:
                negotiated_capabilities[name] = capability.to_dict()
        
        session.negotiated_capabilities = negotiated_capabilities
        session.initialized = True
        
        # Return server information and capabilities
        return {
            "server": {
                "name": "MCPoke Server",
                "version": "1.0.0",
                "description": "A Pokémon API server for MCP"
            },
            "capabilities": negotiated_capabilities
        }
    
    def _handle_shutdown(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Handle the shutdown method.
        
        Args:
            params: Method parameters
            session_id: Session ID
        
        Returns:
            Method result
        """
        # Remove session
        if session_id in self.sessions:
            logger.debug(f"Shutting down session: {session_id}")
            del self.sessions[session_id]
        
        return {"success": True}
    
    def _handle_list_tools(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Handle the listTools method.
        
        Args:
            params: Method parameters
            session_id: Session ID
        
        Returns:
            Method result
        """
        session = self.get_session(session_id)
        
        # Check if session is initialized
        if not session.initialized:
            raise JsonRpcError(
                ERROR_INTERNAL_ERROR,
                "Session not initialized"
            )
        
        # Get tools
        tools = []
        
        for name, tool in self.tools.items():
            tools.append(tool.to_dict())
        
        return {"tools": tools}
    
    def _handle_pokemon_tool(self, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Handle Pokémon tools.
        
        Args:
            params: Method parameters
            session_id: Session ID
        
        Returns:
            Method result
        """
        session = self.get_session(session_id)
        
        # Check if session is initialized
        if not session.initialized:
            raise JsonRpcError(
                ERROR_INTERNAL_ERROR,
                "Session not initialized"
            )
        
        # Route to the appropriate tool handler based on the params
        action = params.get("action")
        
        if action == "get_pokemon":
            return self.server.get_pokemon(params.get("name_or_id"))
        elif action == "search_pokemon":
            return {
                "results": self.server.search_pokemon(
                    params.get("query"),
                    params.get("limit", 10)
                )
            }
        elif action == "get_ability":
            return self.server.get_ability(params.get("name_or_id"))
        elif action == "get_type":
            return self.server.get_type(params.get("name_or_id"))
        elif action == "get_move":
            return self.server.get_move(params.get("name_or_id"))
        elif action == "compare_pokemon":
            return self.server.compare_pokemon(params.get("pokemon_list", []))
        elif action == "get_type_effectiveness":
            return self.server.get_type_effectiveness(
                params.get("attacking_type"),
                params.get("defending_types", [])
            )
        else:
            raise JsonRpcError(
                ERROR_INVALID_PARAMS,
                f"Unknown action: {action}"
            )

class McpStdioHandler:
    """MCP stdio transport handler."""
    
    def __init__(self, protocol_handler: McpProtocolHandler):
        """
        Initialize an MCP stdio handler.
        
        Args:
            protocol_handler: MCP protocol handler
        """
        self.protocol_handler = protocol_handler
        self.session_id = generate_id()
    
    def start(self):
        """Start the stdio handler."""
        logger.info("Starting MCP stdio handler")
        
        try:
            while True:
                # Read request from stdin
                line = sys.stdin.readline()
                if not line:
                    break
                
                # Process request
                response = self.protocol_handler.handle_request(line.strip(), self.session_id)
                
                # Write response to stdout
                if response is not None:
                    sys.stdout.write(response + "\n")
                    sys.stdout.flush()
        except KeyboardInterrupt:
            logger.info("MCP stdio handler interrupted")
        except Exception as e:
            logger.exception(f"Error in MCP stdio handler: {e}")
        finally:
            logger.info("MCP stdio handler stopped")
