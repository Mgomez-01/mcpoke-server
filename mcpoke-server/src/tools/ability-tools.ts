/**
 * Tools for ability-related functionality
 */
import { tools } from '../server.js';
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { processAbilityData } from '../processors/ability.js';

/**
 * Register ability-related tools
 */
export function registerAbilityTools(): void {
  // Get ability tool
  tools['get_ability'] = async (args: { name_or_id: string }) => {
    try {
      const { name_or_id } = args;
      
      // Validate input
      if (!name_or_id || (typeof name_or_id !== 'string' && typeof name_or_id !== 'number')) {
        throw new Error('Ability name or ID must be provided');
      }

      // Try to get from cache first
      const cacheKey = `ability-processed-${name_or_id.toString().toLowerCase()}`;
      const cachedData = cacheManager.get(cacheKey);
      
      if (cachedData) {
        return cachedData;
      }

      // Fetch ability data
      const abilityData = await pokeApiClient.getAbility(name_or_id);
      
      // Process and return the data
      const processedData = await processAbilityData(abilityData);
      
      // Cache the processed data
      cacheManager.set(cacheKey, processedData);
      
      return processedData;
    } catch (error: any) {
      if (error.response && error.response.status === 404) {
        throw new Error(`Ability "${args.name_or_id}" not found`);
      }
      throw new Error(`Failed to get ability information: ${error.message}`);
    }
  };
}
