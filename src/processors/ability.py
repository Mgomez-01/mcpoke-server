"""
Ability data processor.

This module processes ability data from the PokéAPI for consumption by MCP clients.
"""

import logging
from typing import Dict, Any, List

from ..api_client import PokeAPIClient
from ..cache import CacheManager

logger = logging.getLogger('mcpoke-server.processors.ability')

class AbilityProcessor:
    """
    Ability data processor.
    
    This class processes ability data from the PokéAPI for consumption by MCP clients.
    """
    
    def __init__(self, api_client: PokeAPIClient, cache: CacheManager):
        """
        Initialize the ability processor.
        
        Args:
            api_client: PokéAPI client
            cache: Cache manager
        """
        self.api_client = api_client
        self.cache = cache
    
    def get_ability(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about an ability.
        
        Args:
            name_or_id: Name or ID of the ability
        
        Returns:
            Processed ability data
        
        Raises:
            Exception: If the ability could not be fetched
        """
        # Check cache first
        cache_key = f"ability:{name_or_id.lower()}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        try:
            # Fetch ability data
            ability_data = self.api_client.fetch_ability(name_or_id)
            
            # Get English effect text
            effect_entries = ability_data.get("effect_entries", [])
            effect = ""
            short_effect = ""
            
            for entry in effect_entries:
                if entry.get("language", {}).get("name") == "en":
                    effect = entry.get("effect", "")
                    short_effect = entry.get("short_effect", "")
                    break
            
            # Get Pokémon with this ability
            pokemon_with_ability = []
            
            for pokemon in ability_data.get("pokemon", []):
                pokemon_species = pokemon.get("pokemon", {}).get("name", "")
                pokemon_with_ability.append(pokemon_species.capitalize())
            
            # Process data
            processed_data = {
                "id": ability_data.get("id"),
                "name": ability_data.get("name", "").capitalize(),
                "effect": effect,
                "short_effect": short_effect,
                "pokemon": sorted(pokemon_with_ability)
            }
            
            # Cache processed data
            self.cache.set(cache_key, processed_data)
            
            return processed_data
        except Exception as e:
            logger.error(f"Error processing ability {name_or_id}: {e}")
            raise
