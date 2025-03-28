"""
Tests for the PokéAPI client.
"""

import unittest
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api_client import PokeAPIClient

class TestPokeAPIClient(unittest.TestCase):
    """Test cases for the PokéAPI client."""
    
    def setUp(self):
        """Set up the test environment."""
        self.api_client = PokeAPIClient(
            base_url="https://pokeapi.co/api/v2",
            timeout=5
        )
    
    def test_make_request(self):
        """Test making a request to the PokéAPI."""
        # Mock the requests.get method
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 25, "name": "pikachu"}
        mock_response.status_code = 200
        
        with patch('requests.get', return_value=mock_response) as mock_get:
            # Call the method
            response = self.api_client.make_request("pokemon/pikachu")
            
            # Assert the result
            self.assertEqual(response, {"id": 25, "name": "pikachu"})
            mock_get.assert_called_once_with(
                "https://pokeapi.co/api/v2/pokemon/pikachu",
                params=None,
                timeout=5
            )
    
    def test_fetch_pokemon(self):
        """Test fetching a Pokémon from the PokéAPI."""
        # Setup mock return value
        mock_pokemon_data = {"id": 25, "name": "pikachu"}
        
        # Create a mock for make_request
        self.api_client.make_request = MagicMock(return_value=mock_pokemon_data)
        
        # Call the method
        result = self.api_client.fetch_pokemon("pikachu")
        
        # Assert the result
        self.assertEqual(result, mock_pokemon_data)
        self.api_client.make_request.assert_called_once_with("pokemon/pikachu")
    
    def test_fetch_pokemon_species(self):
        """Test fetching a Pokémon species from the PokéAPI."""
        # Setup mock return value
        mock_species_data = {
            "id": 25,
            "name": "pikachu",
            "generation": {"name": "generation-i"}
        }
        
        # Create a mock for make_request
        self.api_client.make_request = MagicMock(return_value=mock_species_data)
        
        # Call the method
        result = self.api_client.fetch_pokemon_species("pikachu")
        
        # Assert the result
        self.assertEqual(result, mock_species_data)
        self.api_client.make_request.assert_called_once_with("pokemon-species/pikachu")

if __name__ == '__main__':
    unittest.main()
