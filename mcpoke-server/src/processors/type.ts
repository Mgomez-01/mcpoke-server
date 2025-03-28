/**
 * Processing functions for type data
 */
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { capitalizeFirstLetter } from '../utils/formatters.js';
import { TypeResponse } from '../api/types.js';

/**
 * Processed type data structure
 */
export interface ProcessedType {
  id: number;
  name: string;
  damage_relations: {
    double_damage_from: string[];
    double_damage_to: string[];
    half_damage_from: string[];
    half_damage_to: string[];
    no_damage_from: string[];
    no_damage_to: string[];
  };
}

/**
 * Process a type response from the API
 * @param typeData The raw type data
 * @returns The processed type data
 */
export function processTypeData(typeData: TypeResponse): ProcessedType {
  return {
    id: typeData.id,
    name: capitalizeFirstLetter(typeData.name),
    damage_relations: {
      double_damage_from: typeData.damage_relations.double_damage_from.map(type => type.name),
      double_damage_to: typeData.damage_relations.double_damage_to.map(type => type.name),
      half_damage_from: typeData.damage_relations.half_damage_from.map(type => type.name),
      half_damage_to: typeData.damage_relations.half_damage_to.map(type => type.name),
      no_damage_from: typeData.damage_relations.no_damage_from.map(type => type.name),
      no_damage_to: typeData.damage_relations.no_damage_to.map(type => type.name)
    }
  };
}

/**
 * Calculate the effectiveness of an attacking type against defending types
 * @param attackingType The attacking type
 * @param defendingTypes The defending types
 * @returns The type effectiveness data
 */
export async function calculateTypeEffectiveness(
  attackingType: string,
  defendingTypes: string[]
): Promise<{
  attacking_type: string;
  defending_types: string[];
  effectiveness: number;
  description: string;
}> {
  // Get attacking type data
  const typeData = await cacheManager.getOrSet<TypeResponse>(
    `type-${attackingType.toLowerCase()}`,
    () => pokeApiClient.getType(attackingType.toLowerCase())
  );
  
  const processedType = processTypeData(typeData);
  
  // Calculate effectiveness for each defending type
  let effectiveness = 1.0;
  
  for (const defendingType of defendingTypes) {
    const lowerDefType = defendingType.toLowerCase();
    
    if (processedType.damage_relations.double_damage_to.includes(lowerDefType)) {
      effectiveness *= 2.0;
    } else if (processedType.damage_relations.half_damage_to.includes(lowerDefType)) {
      effectiveness *= 0.5;
    } else if (processedType.damage_relations.no_damage_to.includes(lowerDefType)) {
      effectiveness = 0;
      break; // No need to continue if there's no effect
    }
  }
  
  // Determine description based on effectiveness
  let description = 'Normally effective';
  
  if (effectiveness === 0) {
    description = 'No effect';
  } else if (effectiveness < 1) {
    description = 'Not very effective';
  } else if (effectiveness > 1) {
    description = 'Super effective';
  }
  
  return {
    attacking_type: capitalizeFirstLetter(attackingType),
    defending_types: defendingTypes.map(type => capitalizeFirstLetter(type)),
    effectiveness,
    description
  };
}
