/**
 * Tools for type-related functionality
 */
import { tools } from '../server.js';
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { processTypeData, calculateTypeEffectiveness } from '../processors/type.js';
import { isValidTypeName } from '../utils/validators.js';

/**
 * Register type-related tools
 */
export function registerTypeTools(): void {
  // Get type tool
  tools['get_type'] = async (args: { name_or_id: string }) => {
    try {
      const { name_or_id } = args;
      
      // Validate input
      if (!name_or_id || (typeof name_or_id !== 'string' && typeof name_or_id !== 'number')) {
        throw new Error('Type name or ID must be provided');
      }

      // Try to get from cache first
      const cacheKey = `type-processed-${name_or_id.toString().toLowerCase()}`;
      const cachedData = cacheManager.get(cacheKey);
      
      if (cachedData) {
        return cachedData;
      }

      // Fetch type data
      const typeData = await pokeApiClient.getType(name_or_id);
      
      // Process and return the data
      const processedData = processTypeData(typeData);
      
      // Cache the processed data
      cacheManager.set(cacheKey, processedData);
      
      return processedData;
    } catch (error: any) {
      if (error.response && error.response.status === 404) {
        throw new Error(`Type "${args.name_or_id}" not found`);
      }
      throw new Error(`Failed to get type information: ${error.message}`);
    }
  };

  // Get type effectiveness tool
  tools['get_type_effectiveness'] = async (args: { attacking_type: string, defending_types: string[] }) => {
    try {
      const { attacking_type, defending_types } = args;
      
      // Validate input
      if (!isValidTypeName(attacking_type)) {
        throw new Error(`Invalid attacking type: ${attacking_type}`);
      }

      if (!Array.isArray(defending_types) || defending_types.length === 0) {
        throw new Error('At least one defending type must be provided');
      }

      for (const type of defending_types) {
        if (!isValidTypeName(type)) {
          throw new Error(`Invalid defending type: ${type}`);
        }
      }

      // Calculate and return type effectiveness
      return await calculateTypeEffectiveness(attacking_type, defending_types);
    } catch (error: any) {
      throw new Error(`Failed to calculate type effectiveness: ${error.message}`);
    }
  };
}
