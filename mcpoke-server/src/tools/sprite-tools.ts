/**
 * Tools for sprite-related functionality
 */
import { tools } from '../server.js';
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { isValidPokemonNameOrId } from '../utils/validators.js';
import {
  downloadAndCachePokemonSprites,
  getPokemonSpriteUrls,
  spriteExistsLocally,
  getFrontDefaultSpritePath,
  getFrontShinySpritePath,
  getOfficialArtworkPath
} from '../utils/images/image-manager.js';

/**
 * Register sprite-related tools
 */
export function registerSpriteTools(): void {
  // Download all sprites for a Pokémon
  tools['download_sprites'] = async (args: { name_or_id: string }) => {
    try {
      const { name_or_id } = args;
      
      // Validate input
      if (!isValidPokemonNameOrId(name_or_id)) {
        throw new Error(`Invalid Pokémon name or ID: ${name_or_id}`);
      }

      // Fetch Pokémon data
      const pokemonData = await pokeApiClient.getPokemon(name_or_id);
      
      // Prepare sprites data
      const sprites = {
        front_default: pokemonData.sprites.front_default,
        front_shiny: pokemonData.sprites.front_shiny,
        official_artwork: pokemonData.sprites.other?.['official-artwork']?.front_default || null
      };
      
      // Download the sprites
      const localPaths = await downloadAndCachePokemonSprites(pokemonData.id, sprites);
      
      // Get data URLs
      const dataUrls = getPokemonSpriteUrls(pokemonData.id);
      
      return {
        id: pokemonData.id,
        name: pokemonData.name,
        sprites: {
          ...sprites,
          data_urls: dataUrls
        }
      };
    } catch (error: any) {
      if (error.response && error.response.status === 404) {
        throw new Error(`Pokémon "${args.name_or_id}" not found`);
      }
      throw new Error(`Failed to download sprites: ${error.message}`);
    }
  };
  
  // Check sprite cache status
  tools['check_sprite_cache'] = async (args: { name_or_id: string }) => {
    try {
      const { name_or_id } = args;
      
      // Validate input
      if (!isValidPokemonNameOrId(name_or_id)) {
        throw new Error(`Invalid Pokémon name or ID: ${name_or_id}`);
      }

      // Fetch Pokémon data to get the ID
      const pokemonData = await pokeApiClient.getPokemon(name_or_id);
      const id = pokemonData.id;
      
      // Check if sprites exist locally
      const frontDefaultPath = getFrontDefaultSpritePath(id);
      const frontShinyPath = getFrontShinySpritePath(id);
      const officialArtworkPath = getOfficialArtworkPath(id);
      
      const frontDefaultExists = spriteExistsLocally(frontDefaultPath);
      const frontShinyExists = spriteExistsLocally(frontShinyPath);
      const officialArtworkExists = spriteExistsLocally(officialArtworkPath);
      
      return {
        id,
        name: pokemonData.name,
        cached_sprites: {
          front_default: frontDefaultExists,
          front_shiny: frontShinyExists,
          official_artwork: officialArtworkExists
        }
      };
    } catch (error: any) {
      if (error.response && error.response.status === 404) {
        throw new Error(`Pokémon "${args.name_or_id}" not found`);
      }
      throw new Error(`Failed to check sprite cache: ${error.message}`);
    }
  };
}
