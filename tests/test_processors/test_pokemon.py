"""
Tests for the Pokémon processor.
"""

import unittest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.processors.pokemon import PokemonProcessor

class TestPokemonProcessor(unittest.TestCase):
    """Test cases for the Pokémon processor."""
    
    def setUp(self):
        """Set up the test environment."""
        self.mock_api_client = MagicMock()
        self.mock_cache = MagicMock()
        self.processor = PokemonProcessor(self.mock_api_client, self.mock_cache)
        
        # Sample Pokémon data
        self.sample_pokemon_data = {
            "id": 25,
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "types": [
                {"type": {"name": "electric"}}
            ],
            "abilities": [
                {"ability": {"name": "static"}, "is_hidden": False},
                {"ability": {"name": "lightning-rod"}, "is_hidden": True}
            ],
            "stats": [
                {"base_stat": 35, "stat": {"name": "hp"}},
                {"base_stat": 55, "stat": {"name": "attack"}},
                {"base_stat": 40, "stat": {"name": "defense"}},
                {"base_stat": 50, "stat": {"name": "special-attack"}},
                {"base_stat": 50, "stat": {"name": "special-defense"}},
                {"base_stat": 90, "stat": {"name": "speed"}}
            ],
            "sprites": {
                "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
                "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/25.png",
                "other": {
                    "official-artwork": {
                        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
                    }
                }
            },
            "species": {
                "url": "https://pokeapi.co/api/v2/pokemon-species/25/"
            }
        }
        
        # Sample species data
        self.sample_species_data = {
            "id": 25,
            "name": "pikachu",
            "generation": {
                "name": "generation-i"
            },
            "flavor_text_entries": [
                {
                    "flavor_text": "When several of\nthese POKéMON\ngather, their\felectricity could\nbuild and cause\nlightning storms.",
                    "language": {
                        "name": "en"
                    },
                    "version": {
                        "name": "yellow"
                    }
                }
            ],
            "evolution_chain": {
                "url": "https://pokeapi.co/api/v2/evolution-chain/10/"
            }
        }
        
        # Sample evolution chain data
        self.sample_evolution_chain = {
            "chain": {
                "species": {
                    "name": "pichu"
                },
                "evolves_to": [
                    {
                        "species": {
                            "name": "pikachu"
                        },
                        "evolution_details": [
                            {
                                "trigger": {
                                    "name": "level-up"
                                },
                                "min_happiness": 220
                            }
                        ],
                        "evolves_to": [
                            {
                                "species": {
                                    "name": "raichu"
                                },
                                "evolution_details": [
                                    {
                                        "trigger": {
                                            "name": "item"
                                        },
                                        "item": {
                                            "name": "thunder-stone"
                                        }
                                    }
                                ],
                                "evolves_to": []
                            }
                        ]
                    }
                ]
            }
        }
    
    def test_get_pokemon(self):
        """Test getting Pokémon information."""
        # Mock the API responses
        self.mock_api_client.fetch_pokemon.return_value = self.sample_pokemon_data
        self.mock_api_client.fetch_pokemon_species.return_value = self.sample_species_data
        self.mock_api_client.fetch_evolution_chain.return_value = self.sample_evolution_chain
        
        # Check if the data is in the cache
        self.mock_cache.get.return_value = None
        
        # Call the method
        result = self.processor.get_pokemon("pikachu")
        
        # Assert the API was called
        self.mock_api_client.fetch_pokemon.assert_called_once_with("pikachu")
        self.mock_api_client.fetch_pokemon_species.assert_called_once_with("pikachu")
        
        # Assert the result is cached
        self.mock_cache.set.assert_called_once()
    
    def test_get_pokemon_from_cache(self):
        """Test getting Pokémon information from the cache."""
        # Setup mock cache response
        cached_data = {
            "id": 25,
            "name": "Pikachu",
            "types": ["electric"]
        }
        self.mock_cache.get.return_value = cached_data
        
        # Call the method
        result = self.processor.get_pokemon("pikachu")
        
        # Assert the result
        self.assertEqual(result, cached_data)
        
        # Assert the API was not called
        self.mock_api_client.fetch_pokemon.assert_not_called()
        self.mock_api_client.fetch_pokemon_species.assert_not_called()

if __name__ == '__main__':
    unittest.main()
