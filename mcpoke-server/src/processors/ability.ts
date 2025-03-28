/**
 * Processing functions for ability data
 */
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { capitalizeFirstLetter } from '../utils/formatters.js';
import { AbilityResponse } from '../api/types.js';

/**
 * Processed ability data structure
 */
export interface ProcessedAbility {
  id: number;
  name: string;
  effect: string;
  short_effect: string;
  pokemon: string[];
}

/**
 * Process an ability response from the API
 * @param abilityData The raw ability data
 * @returns The processed ability data
 */
export async function processAbilityData(abilityData: AbilityResponse): Promise<ProcessedAbility> {
  // Get English effect entries
  const effectEntry = abilityData.effect_entries.find(
    entry => entry.language.name === 'en'
  );

  // Get Pokémon names
  const pokemonNames = abilityData.pokemon.map(
    entry => capitalizeFirstLetter(entry.pokemon.name)
  );

  return {
    id: abilityData.id,
    name: capitalizeFirstLetter(abilityData.name),
    effect: effectEntry?.effect || 'No effect information available.',
    short_effect: effectEntry?.short_effect || 'No short effect information available.',
    pokemon: pokemonNames
  };
}
