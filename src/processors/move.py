"""
Move data processor.

This module processes move data from the PokéAPI for consumption by MCP clients.
"""

import logging
from typing import Dict, Any, List

from ..api_client import PokeAPIClient
from ..cache import CacheManager

logger = logging.getLogger('mcpoke-server.processors.move')

class MoveProcessor:
    """
    Move data processor.
    
    This class processes move data from the PokéAPI for consumption by MCP clients.
    """
    
    def __init__(self, api_client: PokeAPIClient, cache: CacheManager):
        """
        Initialize the move processor.
        
        Args:
            api_client: PokéAPI client
            cache: Cache manager
        """
        self.api_client = api_client
        self.cache = cache
    
    def get_move(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a move.
        
        Args:
            name_or_id: Name or ID of the move
        
        Returns:
            Processed move data
        
        Raises:
            Exception: If the move could not be fetched
        """
        # Check cache first
        cache_key = f"move:{name_or_id.lower()}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        try:
            # Fetch move data
            move_data = self.api_client.fetch_move(name_or_id)
            
            # Get English effect text
            effect_entries = move_data.get("effect_entries", [])
            effect = ""
            short_effect = ""
            
            for entry in effect_entries:
                if entry.get("language", {}).get("name") == "en":
                    effect = entry.get("effect", "")
                    short_effect = entry.get("short_effect", "")
                    break
            
            # Process effect text
            effect_chance = move_data.get("effect_chance")
            
            if effect_chance is not None:
                effect = effect.replace("$effect_chance", str(effect_chance))
                short_effect = short_effect.replace("$effect_chance", str(effect_chance))
            
            # Process data
            processed_data = {
                "id": move_data.get("id"),
                "name": move_data.get("name", "").replace("-", " ").title(),
                "type": move_data.get("type", {}).get("name", "").capitalize(),
                "power": move_data.get("power"),
                "pp": move_data.get("pp"),
                "accuracy": move_data.get("accuracy"),
                "damage_class": move_data.get("damage_class", {}).get("name", "").capitalize(),
                "effect": effect,
                "short_effect": short_effect,
                "effect_chance": effect_chance
            }
            
            # Cache processed data
            self.cache.set(cache_key, processed_data)
            
            return processed_data
        except Exception as e:
            logger.error(f"Error processing move {name_or_id}: {e}")
            raise
