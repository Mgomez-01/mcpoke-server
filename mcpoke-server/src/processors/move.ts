/**
 * Processing functions for move data
 */
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { capitalizeFirstLetter } from '../utils/formatters.js';
import { MoveResponse } from '../api/types.js';

/**
 * Processed move data structure
 */
export interface ProcessedMove {
  id: number;
  name: string;
  type: string;
  power: number | null;
  pp: number | null;
  accuracy: number | null;
  damage_class: string;
  effect: string;
  short_effect: string;
  effect_chance: number | null;
}

/**
 * Process a move response from the API
 * @param moveData The raw move data
 * @returns The processed move data
 */
export function processMoveData(moveData: MoveResponse): ProcessedMove {
  // Get English effect entries
  const effectEntry = moveData.effect_entries.find(
    entry => entry.language.name === 'en'
  );

  // Process effect text to include effect chance
  let effect = effectEntry?.effect || 'No effect information available.';
  let shortEffect = effectEntry?.short_effect || 'No short effect information available.';
  
  // Replace $effect_chance with the actual chance
  if (moveData.effect_chance !== null) {
    effect = effect.replace(/\$effect_chance/g, moveData.effect_chance.toString());
    shortEffect = shortEffect.replace(/\$effect_chance/g, moveData.effect_chance.toString());
  }

  return {
    id: moveData.id,
    name: capitalizeFirstLetter(moveData.name),
    type: capitalizeFirstLetter(moveData.type.name),
    power: moveData.power,
    pp: moveData.pp,
    accuracy: moveData.accuracy,
    damage_class: moveData.damage_class ? capitalizeFirstLetter(moveData.damage_class.name) : 'Unknown',
    effect,
    short_effect: shortEffect,
    effect_chance: moveData.effect_chance
  };
}
