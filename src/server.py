"""
MCPoke Server implementation.

This module implements the Model Context Protocol (MCP) server for the Pokémon API.
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional, List

from .api_client import PokeAPIClient
from .cache import CacheManager
from .processors.pokemon import PokemonProcessor
from .processors.ability import AbilityProcessor
from .processors.move import MoveProcessor
from .processors.type import TypeProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcpoke-server')

class MCPokeRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the MCPoke Server."""
    
    def __init__(self, *args, **kwargs):
        self.server_instance = args[2]
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            request = json.loads(post_data.decode('utf-8'))
            response = self.server_instance.handle_mcp_request(request)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f"Error processing request: {str(e)}"
            }).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override log_message to use our logger."""
        logger.info(f"{self.client_address[0]} - {format % args}")

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
        if config["server"]["debug"]:
            logger.setLevel(logging.DEBUG)
    
    def start(self):
        """Start the server."""
        host = self.config["server"]["host"]
        port = self.config["server"]["port"]
        
        server = HTTPServer((host, port), lambda *args: MCPokeRequestHandler(*args, self))
        logger.info(f"Starting MCPoke Server on {host}:{port}")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server shutting down...")
        finally:
            server.server_close()
    
    def handle_mcp_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an MCP request.
        
        Args:
            request: MCP request dictionary
        
        Returns:
            Response dictionary
        """
        command = request.get("command")
        
        if not command:
            raise ValueError("No command specified in the request")
        
        # Route the command to the appropriate handler
        if command == "get_pokemon":
            return self.get_pokemon(request.get("name_or_id"))
        elif command == "search_pokemon":
            return self.search_pokemon(
                request.get("query"),
                request.get("limit", 10)
            )
        elif command == "get_ability":
            return self.get_ability(request.get("name_or_id"))
        elif command == "get_type":
            return self.get_type(request.get("name_or_id"))
        elif command == "get_move":
            return self.get_move(request.get("name_or_id"))
        elif command == "compare_pokemon":
            return self.compare_pokemon(request.get("pokemon_list", []))
        elif command == "get_type_effectiveness":
            return self.get_type_effectiveness(
                request.get("attacking_type"),
                request.get("defending_types", [])
            )
        else:
            raise ValueError(f"Unknown command: {command}")
    
    def get_pokemon(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a Pokémon.
        
        Args:
            name_or_id: Name or ID of the Pokémon
        
        Returns:
            Pokémon information
        """
        # This is a skeleton implementation. We'll just pass for now.
        pass
    
    def search_pokemon(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for Pokémon by name.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
        
        Returns:
            List of matching Pokémon
        """
        # This is a skeleton implementation. We'll just pass for now.
        pass
    
    def get_ability(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about an ability.
        
        Args:
            name_or_id: Name or ID of the ability
        
        Returns:
            Ability information
        """
        # This is a skeleton implementation. We'll just pass for now.
        pass
    
    def get_type(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a type.
        
        Args:
            name_or_id: Name or ID of the type
        
        Returns:
            Type information
        """
        # This is a skeleton implementation. We'll just pass for now.
        pass
    
    def get_move(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a move.
        
        Args:
            name_or_id: Name or ID of the move
        
        Returns:
            Move information
        """
        # This is a skeleton implementation. We'll just pass for now.
        pass
    
    def compare_pokemon(self, pokemon_list: List[str]) -> Dict[str, Any]:
        """
        Compare multiple Pokémon.
        
        Args:
            pokemon_list: List of Pokémon names or IDs
        
        Returns:
            Comparison information
        """
        # This is a skeleton implementation. We'll just pass for now.
        pass
    
    def get_type_effectiveness(self, attacking_type: str, defending_types: List[str]) -> Dict[str, Any]:
        """
        Calculate type effectiveness.
        
        Args:
            attacking_type: Attacking type
            defending_types: List of defending types
        
        Returns:
            Type effectiveness information
        """
        # This is a skeleton implementation. We'll just pass for now.
        pass
