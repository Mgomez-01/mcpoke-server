"""
Pokémon data processor.

This module processes Pokémon data from the PokéAPI for consumption by MCP clients.
"""

import logging
from typing import Dict, Any, List

from ..api_client import PokeAPIClient
from ..cache import CacheManager

logger = logging.getLogger('mcpoke-server.processors.pokemon')

class PokemonProcessor:
    """
    Pokémon data processor.
    
    This class processes Pokémon data from the PokéAPI for consumption by MCP clients.
    """
    
    def __init__(self, api_client: PokeAPIClient, cache: CacheManager):
        """
        Initialize the Pokémon processor.
        
        Args:
            api_client: PokéAPI client
            cache: Cache manager
        """
        self.api_client = api_client
        self.cache = cache
    
    def get_pokemon(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a Pokémon.
        
        Args:
            name_or_id: Name or ID of the Pokémon
        
        Returns:
            Processed Pokémon data
        
        Raises:
            Exception: If the Pokémon could not be fetched
        """
        # Check cache first
        cache_key = f"pokemon:{name_or_id.lower()}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        try:
            # Fetch Pokémon data
            pokemon_data = self.api_client.fetch_pokemon(name_or_id)
            
            # Fetch species data for additional information
            species_url = pokemon_data.get("species", {}).get("url", "")
            species_parts = species_url.split("/")
            
            if len(species_parts) > 1:
                species_id = species_parts[-2]
                species_data = self.api_client.fetch_pokemon_species(species_id)
            else:
                species_data = {}
            
            # Process data
            processed_data = {
                "id": pokemon_data.get("id"),
                "name": pokemon_data.get("name", "").capitalize(),
                "types": [
                    t.get("type", {}).get("name")
                    for t in pokemon_data.get("types", [])
                ],
                "height": pokemon_data.get("height", 0) / 10 if pokemon_data.get("height") is not None else None,  # Convert to meters
                "weight": pokemon_data.get("weight", 0) / 10 if pokemon_data.get("weight") is not None else None,  # Convert to kg
                "abilities": [
                    {
                        "name": a.get("ability", {}).get("name", "").replace("-", " ").title(),
                        "is_hidden": a.get("is_hidden", False)
                    }
                    for a in pokemon_data.get("abilities", [])
                ],
                "stats": {
                    s.get("stat", {}).get("name"): s.get("base_stat")
                    for s in pokemon_data.get("stats", [])
                },
                "sprites": {
                    "front_default": pokemon_data.get("sprites", {}).get("front_default"),
                    "front_shiny": pokemon_data.get("sprites", {}).get("front_shiny"),
                    "official_artwork": pokemon_data.get("sprites", {}).get("other", {}).get("official-artwork", {}).get("front_default")
                }
            }
            
            # Add species data if available
            if species_data:
                # Get English flavor text (description)
                flavor_text = ""
                
                for entry in species_data.get("flavor_text_entries", []):
                    if entry.get("language", {}).get("name") == "en":
                        flavor_text = entry.get("flavor_text", "").replace("\n", " ").replace("\f", " ")
                        break
                
                processed_data["description"] = flavor_text
                
                # Add generation
                processed_data["generation"] = species_data.get("generation", {}).get("name", "").replace("-", " ").title()
                
                # Add evolution chain if available
                evolution_url = species_data.get("evolution_chain", {}).get("url", "")
                evolution_parts = evolution_url.split("/")
                
                if len(evolution_parts) > 1:
                    evolution_id = evolution_parts[-2]
                    evolution_data = self.api_client.fetch_evolution_chain(evolution_id)
                    
                    if evolution_data:
                        processed_data["evolution_chain"] = self._process_evolution_chain(evolution_data)
            
            # Cache processed data
            self.cache.set(cache_key, processed_data)
            
            return processed_data
        except Exception as e:
            logger.error(f"Error processing Pokémon {name_or_id}: {e}")
            raise
    
    def search_pokemon(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for Pokémon by name.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
        
        Returns:
            List of matching Pokémon
        
        Raises:
            Exception: If the search failed
        """
        # Check cache first
        cache_key = f"pokemon_search:{query.lower()}:{limit}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        try:
            # Fetch all Pokémon
            all_pokemon = self.api_client.search_all_pokemon()
            
            # Filter by name
            results = []
            query = query.lower()
            
            for pokemon in all_pokemon.get("results", []):
                name = pokemon.get("name", "")
                
                if query in name:
                    # Extract ID from URL
                    url = pokemon.get("url", "")
                    parts = url.split("/")
                    pokemon_id = parts[-2] if len(parts) > 1 else None
                    
                    if pokemon_id:
                        # Get sprite URL
                        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
                        
                        # Fetch types if needed
                        types = []
                        
                        try:
                            pokemon_data = self.api_client.fetch_pokemon(pokemon_id)
                            types = [
                                t.get("type", {}).get("name")
                                for t in pokemon_data.get("types", [])
                            ]
                        except Exception:
                            # Ignore errors, just leave types empty
                            pass
                        
                        # Add to results
                        results.append({
                            "id": int(pokemon_id),
                            "name": name.capitalize(),
                            "types": types,
                            "sprite": sprite_url
                        })
                        
                        # Check limit
                        if len(results) >= limit:
                            break
            
            # Cache results
            self.cache.set(cache_key, results)
            
            return results
        except Exception as e:
            logger.error(f"Error searching Pokémon: {e}")
            raise
    
    def _process_evolution_chain(self, evolution_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process an evolution chain.
        
        Args:
            evolution_data: Evolution chain data
        
        Returns:
            Processed evolution chain
        """
        chain = []
        
        # Process chain recursively
        def process_chain(chain_data, details=None):
            species = chain_data.get("species", {})
            
            chain.append({
                "name": species.get("name", "").capitalize(),
                "details": details or {}
            })
            
            for evolution in chain_data.get("evolves_to", []):
                evolution_details = evolution.get("evolution_details", [{}])[0]
                
                # Extract evolution details
                details = {}
                
                if evolution_details.get("min_level"):
                    details["method"] = f"Level {evolution_details.get('min_level')}"
                elif evolution_details.get("item"):
                    details["method"] = f"Use {evolution_details.get('item', {}).get('name', '').replace('-', ' ').title()}"
                elif evolution_details.get("trigger"):
                    trigger = evolution_details.get("trigger", {}).get("name", "")
                    
                    if trigger == "trade":
                        details["method"] = "Trade"
                    elif trigger == "level-up":
                        if evolution_details.get("min_happiness"):
                            details["method"] = f"Happiness ({evolution_details.get('min_happiness')}+)"
                        else:
                            details["method"] = "Level up"
                    elif trigger == "use-item":
                        details["method"] = f"Use {evolution_details.get('item', {}).get('name', '').replace('-', ' ').title()}"
                    else:
                        details["method"] = trigger.replace("-", " ").title()
                
                process_chain(evolution, details)
        
        # Start processing from the base chain
        process_chain(evolution_data.get("chain", {}))
        
        return chain
