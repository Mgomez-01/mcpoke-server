/**
 * Tools for Pokémon-related functionality
 */
import { tools } from '../server.js';
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { 
  processPokemonData, 
  processSearchResults, 
  processPokemonComparison
} from '../processors/pokemon.js';
import { isValidLimit, isValidPokemonNameOrId, validatePokemonList } from '../utils/validators.js';

/**
 * Register Pokémon-related tools
 */
export function registerPokemonTools(): void {
  // Get Pokémon tool
  tools['get_pokemon'] = async (args: { name_or_id: string }) => {
    try {
      const { name_or_id } = args;
      
      // Validate input
      if (!isValidPokemonNameOrId(name_or_id)) {
        throw new Error(`Invalid Pokémon name or ID: ${name_or_id}`);
      }

      // Try to get from cache first
      const cacheKey = `pokemon-processed-${name_or_id.toString().toLowerCase()}`;
      const cachedData = cacheManager.get(cacheKey);
      
      if (cachedData) {
        return cachedData;
      }

      // Fetch Pokémon data
      const pokemonData = await pokeApiClient.getPokemon(name_or_id);
      
      // Process and return the data
      const processedData = await processPokemonData(pokemonData);
      
      // Cache the processed data
      cacheManager.set(cacheKey, processedData);
      
      return processedData;
    } catch (error: any) {
      if (error.response && error.response.status === 404) {
        throw new Error(`Pokémon "${args.name_or_id}" not found`);
      }
      throw new Error(`Failed to get Pokémon information: ${error.message}`);
    }
  };

  // Search Pokémon tool
  tools['search_pokemon'] = async (args: { query: string, limit?: number }) => {
    try {
      const { query, limit = 10 } = args;
      
      // Validate input
      if (!query || typeof query !== 'string' || query.trim() === '') {
        throw new Error('Search query cannot be empty');
      }

      if (!isValidLimit(limit)) {
        throw new Error('Limit must be a positive integer not exceeding 100');
      }

      // Search for Pokémon
      const searchResults = await pokeApiClient.searchPokemon(query, limit);
      
      // Process and return the results
      return await processSearchResults(searchResults.results);
    } catch (error: any) {
      throw new Error(`Failed to search for Pokémon: ${error.message}`);
    }
  };

  // Compare Pokémon tool
  tools['compare_pokemon'] = async (args: { pokemon_list: string[] }) => {
    try {
      const { pokemon_list } = args;
      
      // Validate input
      if (!validatePokemonList(pokemon_list)) {
        throw new Error('Invalid Pokémon list. Please provide valid Pokémon names or IDs.');
      }

      if (pokemon_list.length < 2) {
        throw new Error('At least two Pokémon are required for comparison');
      }

      // Fetch and process each Pokémon
      const pokemonPromises = pokemon_list.map(async (nameOrId: string) => {
        const cacheKey = `pokemon-processed-${nameOrId.toString().toLowerCase()}`;
        
        return cacheManager.getOrSet(cacheKey, async () => {
          const pokemonData = await pokeApiClient.getPokemon(nameOrId);
          return processPokemonData(pokemonData);
        });
      });

      const processedPokemon = await Promise.all(pokemonPromises);
      
      // Return the comparison data
      return processPokemonComparison(processedPokemon);
    } catch (error: any) {
      throw new Error(`Failed to compare Pokémon: ${error.message}`);
    }
  };
}
