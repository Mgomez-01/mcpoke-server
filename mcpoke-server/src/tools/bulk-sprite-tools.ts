/**
 * Tools for bulk sprite operations
 */
import { tools } from '../server.js';
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { 
  downloadAndCachePokemonSprites,
  getPokemonSpriteUrls,
  spriteExistsLocally,
  getFrontDefaultSpritePath,
  getFrontShinySpritePath,
  getOfficialArtworkPath
} from '../utils/images/image-manager.js';
import { clearSpriteCache } from '../utils/images/clear-cache.js';

/**
 * Register bulk sprite-related tools
 */
export function registerBulkSpriteTools(): void {
  // Bulk download sprites for a range of Pokémon
  tools['bulk_download_sprites'] = async (args: { start_id: number, end_id: number, sprite_type?: string }) => {
    try {
      const { start_id, end_id, sprite_type = 'all' } = args;
      
      // Validate input
      if (typeof start_id !== 'number' || start_id < 1) {
        throw new Error(`Invalid start ID: ${start_id}. Must be a positive number.`);
      }
      
      if (typeof end_id !== 'number' || end_id < start_id) {
        throw new Error(`Invalid end ID: ${end_id}. Must be greater than or equal to start ID.`);
      }
      
      if (end_id - start_id > 50) {
        throw new Error('Maximum range for bulk download is 50 Pokémon at a time.');
      }
      
      const validSpriteTypes = ['all', 'default', 'shiny', 'artwork'];
      if (!validSpriteTypes.includes(sprite_type)) {
        throw new Error(`Invalid sprite type: ${sprite_type}. Must be one of: ${validSpriteTypes.join(', ')}`);
      }
      
      // Begin downloading sprites
      const results = {
        total: end_id - start_id + 1,
        completed: 0,
        failed: 0,
        details: [] as Array<{
          id: number;
          name: string;
          success: boolean;
          error?: string;
          sprites?: {
            front_default?: boolean;
            front_shiny?: boolean;
            official_artwork?: boolean;
          };
        }>
      };
      
      // Download sprites for each Pokémon in the range
      for (let id = start_id; id <= end_id; id++) {
        try {
          // Fetch Pokémon data
          const pokemonData = await pokeApiClient.getPokemon(id);
          
          // Prepare sprites data based on selected type
          const sprites: any = {};
          
          if (sprite_type === 'all' || sprite_type === 'default') {
            sprites.front_default = pokemonData.sprites.front_default;
          }
          
          if (sprite_type === 'all' || sprite_type === 'shiny') {
            sprites.front_shiny = pokemonData.sprites.front_shiny;
          }
          
          if (sprite_type === 'all' || sprite_type === 'artwork') {
            sprites.official_artwork = pokemonData.sprites.other?.['official-artwork']?.front_default || null;
          }
          
          // Download the sprites
          const localPaths = await downloadAndCachePokemonSprites(pokemonData.id, sprites);
          
          // Track result
          results.completed++;
          results.details.push({
            id: pokemonData.id,
            name: pokemonData.name,
            success: true,
            sprites: {
              front_default: localPaths.front_default !== null,
              front_shiny: localPaths.front_shiny !== null,
              official_artwork: localPaths.official_artwork !== null
            }
          });
        } catch (error: any) {
          results.failed++;
          results.details.push({
            id,
            name: `pokemon-${id}`,
            success: false,
            error: error.message
          });
        }
      }
      
      return results;
    } catch (error: any) {
      throw new Error(`Failed to bulk download sprites: ${error.message}`);
    }
  };
  
  // Get sprite cache statistics
  tools['get_sprite_cache_stats'] = async () => {
    try {
      // Get a list of all cached sprite files
      const fs = await import('fs');
      const path = await import('path');
      const { fileURLToPath } = await import('url');
      
      const __filename = fileURLToPath(import.meta.url);
      const __dirname = path.dirname(__filename);
      
      const PROJECT_ROOT = path.resolve(__dirname, '../../../');
      const SPRITES_DIR = path.join(PROJECT_ROOT, 'assets/sprites/pokemon');
      const SHINY_SPRITES_DIR = path.join(PROJECT_ROOT, 'assets/sprites/pokemon/shiny');
      const ARTWORK_DIR = path.join(PROJECT_ROOT, 'assets/artwork');
      
      // Check if directories exist
      const spritesExist = fs.existsSync(SPRITES_DIR);
      const shinySpritesExist = fs.existsSync(SHINY_SPRITES_DIR);
      const artworkExists = fs.existsSync(ARTWORK_DIR);
      
      // Count files in each directory
      const regularSpriteCount = spritesExist 
        ? fs.readdirSync(SPRITES_DIR).filter(file => file.endsWith('.png')).length 
        : 0;
        
      const shinySpriteCount = shinySpritesExist 
        ? fs.readdirSync(SHINY_SPRITES_DIR).filter(file => file.endsWith('.png')).length 
        : 0;
        
      const artworkCount = artworkExists 
        ? fs.readdirSync(ARTWORK_DIR).filter(file => file.endsWith('.png')).length 
        : 0;
      
      // Calculate total size of cached files
      let totalSize = 0;
      
      if (spritesExist) {
        const spriteFiles = fs.readdirSync(SPRITES_DIR).filter(file => file.endsWith('.png'));
        for (const file of spriteFiles) {
          const stats = fs.statSync(path.join(SPRITES_DIR, file));
          totalSize += stats.size;
        }
      }
      
      if (shinySpritesExist) {
        const shinyFiles = fs.readdirSync(SHINY_SPRITES_DIR).filter(file => file.endsWith('.png'));
        for (const file of shinyFiles) {
          const stats = fs.statSync(path.join(SHINY_SPRITES_DIR, file));
          totalSize += stats.size;
        }
      }
      
      if (artworkExists) {
        const artworkFiles = fs.readdirSync(ARTWORK_DIR).filter(file => file.endsWith('.png'));
        for (const file of artworkFiles) {
          const stats = fs.statSync(path.join(ARTWORK_DIR, file));
          totalSize += stats.size;
        }
      }
      
      // Format total size
      const formatSize = (bytes: number): string => {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
      };
      
      return {
        total_sprites_cached: regularSpriteCount + shinySpriteCount + artworkCount,
        regular_sprites: regularSpriteCount,
        shiny_sprites: shinySpriteCount,
        artwork: artworkCount,
        total_size: formatSize(totalSize),
        total_size_bytes: totalSize
      };
    } catch (error: any) {
      throw new Error(`Failed to get sprite cache statistics: ${error.message}`);
    }
  };

  // Clear the sprite cache
  tools['clear_sprite_cache'] = async (args: { type?: string }) => {
    try {
      const { type = 'all' } = args;
      
      // Validate input
      const validTypes = ['all', 'regular', 'shiny', 'artwork'];
      if (!validTypes.includes(type)) {
        throw new Error(`Invalid sprite type: ${type}. Must be one of: ${validTypes.join(', ')}`);
      }
      
      // Determine which types to clear
      const clearRegular = type === 'all' || type === 'regular';
      const clearShiny = type === 'all' || type === 'shiny';
      const clearArtwork = type === 'all' || type === 'artwork';
      
      // Clear the cache
      clearSpriteCache(clearRegular, clearShiny, clearArtwork);
      
      return {
        success: true,
        cleared: {
          regular: clearRegular,
          shiny: clearShiny,
          artwork: clearArtwork
        },
        message: `Successfully cleared ${type} sprites from cache.`
      };
    } catch (error: any) {
      throw new Error(`Failed to clear sprite cache: ${error.message}`);
    }
  };
}
