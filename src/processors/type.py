"""
Type data processor.

This module processes type data from the PokéAPI for consumption by MCP clients.
"""

import logging
from typing import Dict, Any, List

from ..api_client import PokeAPIClient
from ..cache import CacheManager

logger = logging.getLogger('mcpoke-server.processors.type')

class TypeProcessor:
    """
    Type data processor.
    
    This class processes type data from the PokéAPI for consumption by MCP clients.
    """
    
    def __init__(self, api_client: PokeAPIClient, cache: CacheManager):
        """
        Initialize the type processor.
        
        Args:
            api_client: PokéAPI client
            cache: Cache manager
        """
        self.api_client = api_client
        self.cache = cache
    
    def get_type(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a type.
        
        Args:
            name_or_id: Name or ID of the type
        
        Returns:
            Processed type data
        
        Raises:
            Exception: If the type could not be fetched
        """
        # Check cache first
        cache_key = f"type:{name_or_id.lower()}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        try:
            # Fetch type data
            type_data = self.api_client.fetch_type(name_or_id)
            
            # Process damage relations
            damage_relations = type_data.get("damage_relations", {})
            
            processed_damage_relations = {
                "double_damage_from": [
                    t.get("name") for t in damage_relations.get("double_damage_from", [])
                ],
                "double_damage_to": [
                    t.get("name") for t in damage_relations.get("double_damage_to", [])
                ],
                "half_damage_from": [
                    t.get("name") for t in damage_relations.get("half_damage_from", [])
                ],
                "half_damage_to": [
                    t.get("name") for t in damage_relations.get("half_damage_to", [])
                ],
                "no_damage_from": [
                    t.get("name") for t in damage_relations.get("no_damage_from", [])
                ],
                "no_damage_to": [
                    t.get("name") for t in damage_relations.get("no_damage_to", [])
                ]
            }
            
            # Process data
            processed_data = {
                "id": type_data.get("id"),
                "name": type_data.get("name", "").capitalize(),
                "damage_relations": processed_damage_relations
            }
            
            # Cache processed data
            self.cache.set(cache_key, processed_data)
            
            return processed_data
        except Exception as e:
            logger.error(f"Error processing type {name_or_id}: {e}")
            raise
