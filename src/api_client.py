"""
PokéAPI client implementation.

This module handles communication with the PokéAPI.
"""

import logging
from typing import Dict, Any, Optional, List
import requests

logger = logging.getLogger('mcpoke-server.api_client')

class PokeAPIClient:
    """
    PokéAPI client for fetching Pokémon data.
    """
    
    def __init__(self, base_url: str = "https://pokeapi.co/api/v2", timeout: int = 10):
        """
        Initialize the PokéAPI client.
        
        Args:
            base_url: Base URL for the PokéAPI
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
    
    def fetch_pokemon(self, name_or_id: str) -> Dict[str, Any]:
        """
        Fetch information about a Pokémon.
        
        Args:
            name_or_id: Name or ID of the Pokémon
        
        Returns:
            Pokémon data
        """
        return self.make_request(f"pokemon/{name_or_id.lower()}")
    
    def fetch_pokemon_species(self, name_or_id: str) -> Dict[str, Any]:
        """
        Fetch species information for a Pokémon.
        
        Args:
            name_or_id: Name or ID of the Pokémon species
        
        Returns:
            Pokémon species data
        """
        return self.make_request(f"pokemon-species/{name_or_id.lower()}")
    
    def fetch_ability(self, name_or_id: str) -> Dict[str, Any]:
        """
        Fetch information about an ability.
        
        Args:
            name_or_id: Name or ID of the ability
        
        Returns:
            Ability data
        """
        return self.make_request(f"ability/{name_or_id.lower()}")
    
    def fetch_type(self, name_or_id: str) -> Dict[str, Any]:
        """
        Fetch information about a type.
        
        Args:
            name_or_id: Name or ID of the type
        
        Returns:
            Type data
        """
        return self.make_request(f"type/{name_or_id.lower()}")
    
    def fetch_move(self, name_or_id: str) -> Dict[str, Any]:
        """
        Fetch information about a move.
        
        Args:
            name_or_id: Name or ID of the move
        
        Returns:
            Move data
        """
        return self.make_request(f"move/{name_or_id.lower()}")
    
    def fetch_evolution_chain(self, chain_id: int) -> Dict[str, Any]:
        """
        Fetch an evolution chain.
        
        Args:
            chain_id: ID of the evolution chain
        
        Returns:
            Evolution chain data
        """
        return self.make_request(f"evolution-chain/{chain_id}")
    
    def search_all_pokemon(self, limit: int = 1000, offset: int = 0) -> Dict[str, Any]:
        """
        Fetch a list of all Pokémon.
        
        Args:
            limit: Maximum number of results to return
            offset: Results offset
        
        Returns:
            List of all Pokémon (paginated)
        """
        return self.make_request("pokemon", params={"limit": limit, "offset": offset})
    
    def make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the PokéAPI.
        
        Args:
            endpoint: API endpoint (without the base URL)
            params: Query parameters
        
        Returns:
            API response data
        
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            logger.debug(f"Making request to {url}")
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
