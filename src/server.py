"""
MCPoke Server implementation.

This module implements the Model Context Protocol (MCP) server for the Pokémon API.
"""

import json
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional, List, Union, cast, Type

from .api_client import PokeAPIClient
from .cache import CacheManager
from .processors.pokemon import PokemonProcessor
from .processors.ability import AbilityProcessor
from .processors.move import MoveProcessor
from .processors.type import TypeProcessor
from .mcp import McpProtocolHandler, McpStdioHandler, McpTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcpoke-server')

class MCPokeRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the MCPoke Server."""
    
    # Class-level variable to store the server instance
    server_instance = None
    
    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Process as JSON-RPC
            request_str = post_data.decode('utf-8')
            request = json.loads(request_str)
            
            # Extract session ID from multiple possible sources
            session_id = self._get_session_id(request)
            
            # Log the session ID and request method
            method = request.get("method", "unknown")
            logger.debug(f"Request: method={method}, session_id={session_id}")
            
            # Process request
            response = self.server_instance.mcp_protocol_handler.handle_request(request_str, session_id)
            
            # Set session cookie in response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Set-Cookie', f'mcp_session_id={session_id}; Path=/')
            self.end_headers()
            
            if response is not None:
                self.wfile.write(response.encode('utf-8'))
            else:
                self.wfile.write(b"{}")
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": None
            }).encode('utf-8'))
    
    def _get_session_id(self, request: Dict[str, Any]) -> str:
        """
        Get the session ID from the request.
        
        Checks multiple sources in order:
        1. X-MCP-Session-ID header
        2. session_id parameter in the request
        3. session_id cookie
        4. Generate a new ID based on client address
        
        Args:
            request: Request data
        
        Returns:
            Session ID
        """
        # Check header
        header_session_id = self.headers.get('X-MCP-Session-ID')
        if header_session_id:
            return header_session_id
        
        # Check parameter in request
        params = request.get("params", {})
        if isinstance(params, dict) and "session_id" in params:
            return params["session_id"]
        
        # Check cookie
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            for cookie in cookie_header.split(';'):
                cookie = cookie.strip()
                if cookie.startswith('mcp_session_id='):
                    return cookie[len('mcp_session_id='):]
        
        # Generate new ID based on client address
        return f"http-{self.client_address[0]}:{self.client_address[1]}"
    
    def log_message(self, format, *args):
        """Override log_message to use our logger."""
        logger.info(f"{self.client_address[0]} - {format % args}")

def create_handler_class(server_instance) -> Type[MCPokeRequestHandler]:
    """
    Create a request handler class with the server instance.
    
    Args:
        server_instance: Server instance
    
    Returns:
        Request handler class
    """
    # Set the server instance on the class
    MCPokeRequestHandler.server_instance = server_instance
    return MCPokeRequestHandler

class MCPokeServer:
    """
    MCPoke Server implementation.
    
    This class implements the Model Context Protocol (MCP) server for the Pokémon API.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the MCPoke Server.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.api_client = PokeAPIClient(
            base_url=config["api"]["base_url"],
            timeout=config["api"]["timeout"]
        )
        self.cache = CacheManager(
            enabled=config["cache"]["enabled"],
            ttl=config["cache"]["ttl"],
            max_size=config["cache"]["max_size"]
        )
        
        # Initialize processors
        self.pokemon_processor = PokemonProcessor(self.api_client, self.cache)
        self.ability_processor = AbilityProcessor(self.api_client, self.cache)
        self.move_processor = MoveProcessor(self.api_client, self.cache)
        self.type_processor = TypeProcessor(self.api_client, self.cache)
        
        # Set debug level
        if config["server"].get("debug", False):
            logger.setLevel(logging.DEBUG)
        
        # Initialize MCP protocol handler
        self.mcp_protocol_handler = McpProtocolHandler(self)
        
        # Register MCP tools
        self._register_mcp_tools()
    
    def _register_mcp_tools(self):
        """Register MCP tools."""
        # Pokemon tool
        self.mcp_protocol_handler.register_tool(McpTool(
            name="pokemon",
            description="Get information about Pokémon",
            parameters={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": [
                            "get_pokemon",
                            "search_pokemon",
                            "get_ability",
                            "get_type",
                            "get_move",
                            "compare_pokemon",
                            "get_type_effectiveness"
                        ],
                        "description": "Action to perform"
                    },
                    "name_or_id": {
                        "type": "string",
                        "description": "Name or ID of the Pokémon, ability, type, or move"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query for Pokémon"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return"
                    },
                    "pokemon_list": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of Pokémon names or IDs to compare"
                    },
                    "attacking_type": {
                        "type": "string",
                        "description": "Attacking type for type effectiveness calculation"
                    },
                    "defending_types": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Defending types for type effectiveness calculation"
                    }
                },
                "required": ["action"]
            },
            handler=self._handle_pokemon_tool
        ))
    
    def _handle_pokemon_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Pokémon tool.
        
        Args:
            params: Tool parameters
        
        Returns:
            Tool result
        """
        action = params.get("action")
        
        if action == "get_pokemon":
            return self.get_pokemon(params.get("name_or_id"))
        elif action == "search_pokemon":
            return {
                "results": self.search_pokemon(
                    params.get("query"),
                    params.get("limit", 10)
                )
            }
        elif action == "get_ability":
            return self.get_ability(params.get("name_or_id"))
        elif action == "get_type":
            return self.get_type(params.get("name_or_id"))
        elif action == "get_move":
            return self.get_move(params.get("name_or_id"))
        elif action == "compare_pokemon":
            return self.compare_pokemon(params.get("pokemon_list", []))
        elif action == "get_type_effectiveness":
            return self.get_type_effectiveness(
                params.get("attacking_type"),
                params.get("defending_types", [])
            )
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def start(self):
        """Start the server."""
        # Determine transport modes
        transports = self.config.get("transport", ["http", "stdio"])
        
        if "stdio" in transports:
            # Start stdio handler in a separate thread
            stdio_thread = threading.Thread(
                target=self._start_stdio_handler,
                daemon=True
            )
            stdio_thread.start()
        
        if "http" in transports:
            # Start HTTP server
            self._start_http_server()
    
    def _start_stdio_handler(self):
        """Start the stdio handler."""
        logger.info("Starting stdio handler")
        stdio_handler = McpStdioHandler(self.mcp_protocol_handler)
        stdio_handler.start()
    
    def _start_http_server(self):
        """Start the HTTP server."""
        host = self.config["server"].get("host", "0.0.0.0")
        port = self.config["server"].get("port", 8000)
        
        # Create handler class with this server instance
        handler_class = create_handler_class(self)
        
        server = HTTPServer((host, port), handler_class)
        logger.info(f"Starting HTTP server on {host}:{port}")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server shutting down...")
        finally:
            server.server_close()
    
    def get_pokemon(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a Pokémon.
        
        Args:
            name_or_id: Name or ID of the Pokémon
        
        Returns:
            Pokémon information
        """
        try:
            return self.pokemon_processor.get_pokemon(name_or_id)
        except Exception as e:
            logger.error(f"Error getting Pokémon: {e}")
            return {"error": str(e)}
    
    def search_pokemon(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for Pokémon by name.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
        
        Returns:
            List of matching Pokémon
        """
        try:
            return self.pokemon_processor.search_pokemon(query, limit)
        except Exception as e:
            logger.error(f"Error searching Pokémon: {e}")
            return [{"error": str(e)}]
    
    def get_ability(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about an ability.
        
        Args:
            name_or_id: Name or ID of the ability
        
        Returns:
            Ability information
        """
        try:
            return self.ability_processor.get_ability(name_or_id)
        except Exception as e:
            logger.error(f"Error getting ability: {e}")
            return {"error": str(e)}
    
    def get_type(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a type.
        
        Args:
            name_or_id: Name or ID of the type
        
        Returns:
            Type information
        """
        try:
            return self.type_processor.get_type(name_or_id)
        except Exception as e:
            logger.error(f"Error getting type: {e}")
            return {"error": str(e)}
    
    def get_move(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a move.
        
        Args:
            name_or_id: Name or ID of the move
        
        Returns:
            Move information
        """
        try:
            return self.move_processor.get_move(name_or_id)
        except Exception as e:
            logger.error(f"Error getting move: {e}")
            return {"error": str(e)}
    
    def compare_pokemon(self, pokemon_list: List[str]) -> Dict[str, Any]:
        """
        Compare multiple Pokémon.
        
        Args:
            pokemon_list: List of Pokémon names or IDs
        
        Returns:
            Comparison information
        """
        try:
            # Get information about each Pokémon
            pokemon_data = []
            
            for name_or_id in pokemon_list:
                pokemon = self.get_pokemon(name_or_id)
                pokemon_data.append(pokemon)
            
            # Compare stats
            stat_comparison = {}
            
            if pokemon_data:
                stats = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
                
                for stat in stats:
                    stat_comparison[stat] = {}
                    
                    for pokemon in pokemon_data:
                        if "stats" in pokemon:
                            for pokemon_stat in pokemon.get("stats", {}):
                                if pokemon_stat.get("stat", {}).get("name") == stat:
                                    stat_comparison[stat][pokemon.get("name")] = pokemon_stat.get("base_stat", 0)
            
            # Calculate type advantages
            type_advantages = {}
            
            for i, attacker in enumerate(pokemon_data):
                for j, defender in enumerate(pokemon_data):
                    if i != j:
                        key = f"{attacker.get('name')} vs {defender.get('name')}"
                        type_advantages[key] = {
                            "type_effectiveness": {}
                        }
                        
                        # Calculate effectiveness for each type
                        attacker_types = [t.get("type", {}).get("name") for t in attacker.get("types", [])]
                        defender_types = [t.get("type", {}).get("name") for t in defender.get("types", [])]
                        
                        for attacker_type in attacker_types:
                            effectiveness = self.get_type_effectiveness(attacker_type, defender_types)
                            
                            type_advantages[key]["type_effectiveness"][attacker_type] = {
                                "attacking_type": attacker_type,
                                "defending_types": defender_types,
                                "effectiveness": effectiveness.get("effectiveness", 1.0),
                                "description": effectiveness.get("description", "Normal")
                            }
                        
                        # Calculate average effectiveness
                        if attacker_types:
                            effectiveness_values = [
                                e.get("effectiveness", 1.0)
                                for e in type_advantages[key]["type_effectiveness"].values()
                            ]
                            avg_effectiveness = sum(effectiveness_values) / len(effectiveness_values)
                            
                            type_advantages[key]["average_effectiveness"] = avg_effectiveness
                            
                            # Determine overall description
                            if avg_effectiveness >= 2.0:
                                type_advantages[key]["overall_description"] = "Strong"
                            elif avg_effectiveness <= 0.5:
                                type_advantages[key]["overall_description"] = "Weak"
                            else:
                                type_advantages[key]["overall_description"] = "Neutral"
            
            return {
                "pokemon": pokemon_data,
                "stat_comparison": stat_comparison,
                "type_advantages": type_advantages
            }
        except Exception as e:
            logger.error(f"Error comparing Pokémon: {e}")
            return {"error": str(e)}
    
    def get_type_effectiveness(self, attacking_type: str, defending_types: List[str]) -> Dict[str, Any]:
        """
        Calculate type effectiveness.
        
        Args:
            attacking_type: Attacking type
            defending_types: List of defending types
        
        Returns:
            Type effectiveness information
        """
        try:
            # Get type information
            attacking_type_data = self.get_type(attacking_type)
            
            # Calculate effectiveness
            effectiveness = 1.0
            
            for defending_type in defending_types:
                # Get damage relations
                damage_relations = attacking_type_data.get("damage_relations", {})
                
                # Check double damage
                double_damage_to = [
                    t.get("name") for t in damage_relations.get("double_damage_to", [])
                ]
                
                if defending_type in double_damage_to:
                    effectiveness *= 2.0
                
                # Check half damage
                half_damage_to = [
                    t.get("name") for t in damage_relations.get("half_damage_to", [])
                ]
                
                if defending_type in half_damage_to:
                    effectiveness *= 0.5
                
                # Check no damage
                no_damage_to = [
                    t.get("name") for t in damage_relations.get("no_damage_to", [])
                ]
                
                if defending_type in no_damage_to:
                    effectiveness = 0.0
                    break
            
            # Determine description
            description = "Normally effective"
            
            if effectiveness == 0.0:
                description = "No effect"
            elif effectiveness < 1.0:
                description = "Not very effective"
            elif effectiveness > 1.0:
                description = "Super effective"
            
            return {
                "attacking_type": attacking_type.capitalize(),
                "defending_types": [t.capitalize() for t in defending_types],
                "effectiveness": effectiveness,
                "description": description
            }
        except Exception as e:
            logger.error(f"Error calculating type effectiveness: {e}")
            return {"error": str(e)}
