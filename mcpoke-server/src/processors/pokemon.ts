/**
 * Processing functions for Pokémon data
 */
import { pokeApiClient } from '../api/pokeapi.js';
import { cacheManager } from '../cache/cache-manager.js';
import { capitalizeFirstLetter, cleanDescription } from '../utils/formatters.js';
import { 
  PokemonResponse, 
  PokemonSpeciesResponse, 
  EvolutionChainResponse 
} from '../api/types.js';

/**
 * Processed Pokémon data structure
 */
export interface ProcessedPokemon {
  id: number;
  name: string;
  types: string[];
  height: number;
  weight: number;
  abilities: {
    name: string;
    is_hidden: boolean;
  }[];
  stats: {
    hp: number;
    attack: number;
    defense: number;
    'special-attack': number;
    'special-defense': number;
    speed: number;
  };
  sprites: {
    front_default: string | null;
    front_shiny: string | null;
    official_artwork: string | null;
  };
  description: string;
  generation: string;
  evolution_chain: {
    name: string;
    details: Record<string, any>;
  }[];
}

/**
 * Process a Pokémon response from the API
 * @param pokemonData The raw Pokémon data
 * @param speciesData The raw Pokémon species data
 * @param evolutionData The raw evolution chain data
 * @returns The processed Pokémon data
 */
export async function processPokemonData(
  pokemonData: PokemonResponse,
  speciesData?: PokemonSpeciesResponse,
  evolutionData?: EvolutionChainResponse
): Promise<ProcessedPokemon> {
  // Fetch species data if not provided
  if (!speciesData) {
    speciesData = await cacheManager.getOrSet<PokemonSpeciesResponse>(
      `pokemon-species-${pokemonData.id}`,
      () => pokeApiClient.getPokemonSpecies(pokemonData.id)
    );
  }

  // Fetch evolution chain data if not provided
  if (!evolutionData && speciesData.evolution_chain) {
    const evolutionChainUrl = speciesData.evolution_chain.url;
    const evolutionChainId = parseInt(evolutionChainUrl.split('/').filter(Boolean).pop() || '0');
    
    evolutionData = await cacheManager.getOrSet<EvolutionChainResponse>(
      `evolution-chain-${evolutionChainId}`,
      () => pokeApiClient.getEvolutionChainByUrl(evolutionChainUrl)
    );
  }

  // Get English description
  const description = speciesData.flavor_text_entries
    .find(entry => entry.language.name === 'en')
    ?.flavor_text || '';

  // Process evolution chain
  const evolutionChain = processEvolutionChain(evolutionData);

  // Process stats into an object
  const stats = pokemonData.stats.reduce<Record<string, number>>((acc, stat) => {
    acc[stat.stat.name] = stat.base_stat;
    return acc;
  }, {});

  return {
    id: pokemonData.id,
    name: capitalizeFirstLetter(pokemonData.name),
    types: pokemonData.types.map(type => type.type.name),
    height: pokemonData.height / 10, // Convert to meters
    weight: pokemonData.weight / 10, // Convert to kilograms
    abilities: pokemonData.abilities.map(ability => ({
      name: capitalizeFirstLetter(ability.ability.name),
      is_hidden: ability.is_hidden
    })),
    stats: {
      hp: stats.hp || 0,
      attack: stats.attack || 0,
      defense: stats.defense || 0,
      'special-attack': stats['special-attack'] || 0,
      'special-defense': stats['special-defense'] || 0,
      speed: stats.speed || 0
    },
    sprites: {
      front_default: pokemonData.sprites.front_default,
      front_shiny: pokemonData.sprites.front_shiny,
      official_artwork: pokemonData.sprites.other?.['official-artwork']?.front_default || null
    },
    description: cleanDescription(description),
    generation: capitalizeFirstLetter(speciesData.generation.name.replace('-', ' ')),
    evolution_chain: evolutionChain
  };
}

/**
 * Process the evolution chain data
 * @param evolutionData The raw evolution chain data
 * @returns The processed evolution chain
 */
function processEvolutionChain(evolutionData?: EvolutionChainResponse): { name: string; details: Record<string, any> }[] {
  if (!evolutionData) {
    return [];
  }
  
  const chain: { name: string; details: Record<string, any> }[] = [];
  
  // Process the base form
  chain.push({
    name: capitalizeFirstLetter(evolutionData.chain.species.name),
    details: {}
  });
  
  // Process first evolution
  let evolvesTo = evolutionData.chain.evolves_to;
  while (evolvesTo && evolvesTo.length > 0) {
    const evolution = evolvesTo[0]; // Take the first evolution path
    const details: Record<string, any> = {};
    
    // Process evolution details
    if (evolution.evolution_details && evolution.evolution_details.length > 0) {
      const evolutionDetail = evolution.evolution_details[0];
      
      if (evolutionDetail.min_level) {
        details.method = `Level ${evolutionDetail.min_level}`;
      } else if (evolutionDetail.min_happiness) {
        details.method = `Happiness (${evolutionDetail.min_happiness}+)`;
      } else if (evolutionDetail.item) {
        details.method = `Use ${capitalizeFirstLetter(evolutionDetail.item.name.replace('-', ' '))}`;
      } else if (evolutionDetail.trigger) {
        details.method = capitalizeFirstLetter(evolutionDetail.trigger.name.replace('-', ' '));
      }
    }
    
    chain.push({
      name: capitalizeFirstLetter(evolution.species.name),
      details
    });
    
    // Move to next evolution
    evolvesTo = evolution.evolves_to;
  }
  
  return chain;
}

/**
 * Process search results for Pokémon
 * @param searchResults The search results data
 * @returns The processed search results
 */
export async function processSearchResults(searchResults: { name: string; url: string }[]): Promise<any[]> {
  const processedResults = [];
  
  for (const result of searchResults) {
    // Extract ID from URL
    const id = parseInt(result.url.split('/').filter(Boolean).pop() || '0');
    
    // Get basic data for this Pokémon
    const pokemon = await cacheManager.getOrSet<PokemonResponse>(
      `pokemon-${id}`,
      () => pokeApiClient.getPokemon(id)
    );
    
    processedResults.push({
      id: pokemon.id,
      name: capitalizeFirstLetter(pokemon.name),
      types: pokemon.types.map(type => type.type.name),
      sprite: pokemon.sprites.front_default
    });
  }
  
  return processedResults;
}

/**
 * Process multiple Pokémon for comparison
 * @param pokemonList List of processed Pokémon data
 * @returns Comparison data for the Pokémon
 */
export function processPokemonComparison(pokemonList: ProcessedPokemon[]): any {
  if (pokemonList.length < 2) {
    throw new Error('At least two Pokémon are required for comparison');
  }

  // Create stat comparison
  const statComparison: Record<string, Record<string, number>> = {
    hp: {},
    attack: {},
    defense: {},
    'special-attack': {},
    'special-defense': {},
    speed: {}
  };

  // Fill in stats for each Pokémon
  for (const pokemon of pokemonList) {
    Object.entries(pokemon.stats).forEach(([stat, value]) => {
      statComparison[stat][pokemon.name] = value;
    });
  }

  // Create type advantage comparison
  const typeAdvantages: Record<string, any> = {};

  // Compare each pair of Pokémon
  for (let i = 0; i < pokemonList.length; i++) {
    for (let j = 0; j < pokemonList.length; j++) {
      if (i === j) continue;

      const attacker = pokemonList[i];
      const defender = pokemonList[j];

      const comparisonKey = `${attacker.name} vs ${defender.name}`;
      typeAdvantages[comparisonKey] = {
        type_effectiveness: {},
        average_effectiveness: 0,
        overall_description: ''
      };

      // This is a placeholder - actual type effectiveness would need to be calculated
      // In a full implementation, we would use the type chart data
      typeAdvantages[comparisonKey].overall_description = 'Neutral';
    }
  }

  return {
    pokemon: pokemonList,
    stat_comparison: statComparison,
    type_advantages: typeAdvantages
  };
}
