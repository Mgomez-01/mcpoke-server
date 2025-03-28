"""
Tests for the MCPoke Server.
"""

import json
import unittest
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.server import MCPokeServer

class TestMCPokeServer(unittest.TestCase):
    """Test cases for the MCPoke Server."""
    
    def setUp(self):
        """Set up the test environment."""
        self.config = {
            "server": {
                "host": "127.0.0.1",
                "port": 8000,
                "debug": True
            },
            "api": {
                "base_url": "https://pokeapi.co/api/v2",
                "timeout": 5
            },
            "cache": {
                "enabled": True,
                "ttl": 3600,
                "max_size": 100
            }
        }
        
        # Create mock objects
        self.mock_api_client = MagicMock()
        self.mock_cache = MagicMock()
        self.mock_pokemon_processor = MagicMock()
        self.mock_ability_processor = MagicMock()
        self.mock_move_processor = MagicMock()
        self.mock_type_processor = MagicMock()
        
        # Create patches
        self.api_client_patch = patch('src.api_client.PokeAPIClient', return_value=self.mock_api_client)
        self.cache_patch = patch('src.cache.CacheManager', return_value=self.mock_cache)
        self.pokemon_processor_patch = patch('src.processors.pokemon.PokemonProcessor', return_value=self.mock_pokemon_processor)
        self.ability_processor_patch = patch('src.processors.ability.AbilityProcessor', return_value=self.mock_ability_processor)
        self.move_processor_patch = patch('src.processors.move.MoveProcessor', return_value=self.mock_move_processor)
        self.type_processor_patch = patch('src.processors.type.TypeProcessor', return_value=self.mock_type_processor)
        
        # Start patches
        self.api_client_patch.start()
        self.cache_patch.start()
        self.pokemon_processor_patch.start()
        self.ability_processor_patch.start()
        self.move_processor_patch.start()
        self.type_processor_patch.start()
        
        # Create server instance
        self.server = MCPokeServer(self.config)
    
    def tearDown(self):
        """Clean up the test environment."""
        # Stop patches
        self.api_client_patch.stop()
        self.cache_patch.stop()
        self.pokemon_processor_patch.stop()
        self.ability_processor_patch.stop()
        self.move_processor_patch.stop()
        self.type_processor_patch.stop()
    
    def test_handle_mcp_request_get_pokemon(self):
        """Test handling a get_pokemon request."""
        # Setup mock return value
        expected_result = {"id": 25, "name": "Pikachu"}
        self.mock_pokemon_processor.get_pokemon.return_value = expected_result
        
        # Call the method
        request = {"command": "get_pokemon", "name_or_id": "pikachu"}
        result = self.server.handle_mcp_request(request)
        
        # Assert the result
        self.assertEqual(result, expected_result)
        self.mock_pokemon_processor.get_pokemon.assert_called_once_with("pikachu")
    
    def test_handle_mcp_request_search_pokemon(self):
        """Test handling a search_pokemon request."""
        # Setup mock return value
        expected_result = [{"id": 25, "name": "Pikachu"}]
        self.mock_pokemon_processor.search_pokemon.return_value = expected_result
        
        # Call the method
        request = {"command": "search_pokemon", "query": "pika", "limit": 10}
        result = self.server.handle_mcp_request(request)
        
        # Assert the result
        self.assertEqual(result, expected_result)
        self.mock_pokemon_processor.search_pokemon.assert_called_once_with("pika", 10)
    
    def test_handle_mcp_request_get_ability(self):
        """Test handling a get_ability request."""
        # Setup mock return value
        expected_result = {"id": 9, "name": "Static"}
        self.mock_ability_processor.get_ability.return_value = expected_result
        
        # Call the method
        request = {"command": "get_ability", "name_or_id": "static"}
        result = self.server.handle_mcp_request(request)
        
        # Assert the result
        self.assertEqual(result, expected_result)
        self.mock_ability_processor.get_ability.assert_called_once_with("static")
    
    def test_handle_mcp_request_invalid_command(self):
        """Test handling an invalid command."""
        # Call the method
        request = {"command": "invalid_command"}
        
        # Assert that it raises a ValueError
        with self.assertRaises(ValueError):
            self.server.handle_mcp_request(request)

if __name__ == '__main__':
    unittest.main()
