/**
 * Tools for move-related functionality
 */
import { tools } from '../server.js';
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { processMoveData } from '../processors/move.js';

/**
 * Register move-related tools
 */
export function registerMoveTools(): void {
  // Get move tool
  tools['get_move'] = async (args: { name_or_id: string }) => {
    try {
      const { name_or_id } = args;
      
      // Validate input
      if (!name_or_id || (typeof name_or_id !== 'string' && typeof name_or_id !== 'number')) {
        throw new Error('Move name or ID must be provided');
      }

      // Try to get from cache first
      const cacheKey = `move-processed-${name_or_id.toString().toLowerCase()}`;
      const cachedData = cacheManager.get(cacheKey);
      
      if (cachedData) {
        return cachedData;
      }

      // Fetch move data
      const moveData = await pokeApiClient.getMove(name_or_id);
      
      // Process and return the data
      const processedData = processMoveData(moveData);
      
      // Cache the processed data
      cacheManager.set(cacheKey, processedData);
      
      return processedData;
    } catch (error: any) {
      if (error.response && error.response.status === 404) {
        throw new Error(`Move "${args.name_or_id}" not found`);
      }
      throw new Error(`Failed to get move information: ${error.message}`);
    }
  };
}
