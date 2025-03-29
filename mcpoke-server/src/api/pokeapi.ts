/**
 * PokeAPI client for handling API requests
 */
import axios, { AxiosInstance } from 'axios';
import { debugLog, debugError } from '../utils/debug.js';
import {
  PokemonResponse,
  PokemonSpeciesResponse,
  EvolutionChainResponse,
  AbilityResponse,
  TypeResponse,
  MoveResponse,
  PokemonListResponse
} from './types.js';

/**
 * PokéAPI client for making requests to the PokéAPI
 */
class PokeApiClient {
  private readonly client: AxiosInstance;
  private readonly baseUrl: string;

  /**
   * Create a new PokéAPI client
   * @param baseUrl The base URL for the PokéAPI
   * @param timeout Timeout in seconds for API requests
   */
  constructor(baseUrl: string = 'https://pokeapi.co/api/v2', timeout: number = 10) {
    this.baseUrl = baseUrl;
    this.client = axios.create({
      baseURL: baseUrl,
      timeout: timeout * 1000 // Convert to milliseconds
    });
  }

  /**
   * Get information about a Pokémon by name or ID
   * @param nameOrId The name or ID of the Pokémon
   * @returns The Pokémon data
   */
  async getPokemon(nameOrId: string | number): Promise<PokemonResponse> {
    try {
      debugLog('PokeAPI', `Requesting Pokémon data for: ${nameOrId}`);
      const response = await this.client.get<PokemonResponse>(`/pokemon/${nameOrId.toString().toLowerCase()}`);
      debugLog('PokeAPI', `Received Pokémon data for: ${nameOrId}`, { id: response.data.id, name: response.data.name });
      return response.data;
    } catch (error) {
      debugError('PokeAPI', error, `Failed to fetch Pokémon: ${nameOrId}`);
      throw error;
    }
  }

  /**
   * Get species information for a Pokémon by name or ID
   * @param nameOrId The name or ID of the Pokémon species
   * @returns The Pokémon species data
   */
  async getPokemonSpecies(nameOrId: string | number): Promise<PokemonSpeciesResponse> {
    const response = await this.client.get<PokemonSpeciesResponse>(`/pokemon-species/${nameOrId.toString().toLowerCase()}`);
    return response.data;
  }

  /**
   * Get the evolution chain for a Pokémon
   * @param id The ID of the evolution chain
   * @returns The evolution chain data
   */
  async getEvolutionChain(id: number): Promise<EvolutionChainResponse> {
    const response = await this.client.get<EvolutionChainResponse>(`/evolution-chain/${id}`);
    return response.data;
  }

  /**
   * Get evolution chain by URL
   * @param url The full URL of the evolution chain
   * @returns The evolution chain data
   */
  async getEvolutionChainByUrl(url: string): Promise<EvolutionChainResponse> {
    const response = await axios.get<EvolutionChainResponse>(url);
    return response.data;
  }

  /**
   * Get information about an ability by name or ID
   * @param nameOrId The name or ID of the ability
   * @returns The ability data
   */
  async getAbility(nameOrId: string | number): Promise<AbilityResponse> {
    const response = await this.client.get<AbilityResponse>(`/ability/${nameOrId.toString().toLowerCase()}`);
    return response.data;
  }

  /**
   * Get information about a type by name or ID
   * @param nameOrId The name or ID of the type
   * @returns The type data
   */
  async getType(nameOrId: string | number): Promise<TypeResponse> {
    const response = await this.client.get<TypeResponse>(`/type/${nameOrId.toString().toLowerCase()}`);
    return response.data;
  }

  /**
   * Get information about a move by name or ID
   * @param nameOrId The name or ID of the move
   * @returns The move data
   */
  async getMove(nameOrId: string | number): Promise<MoveResponse> {
    const response = await this.client.get<MoveResponse>(`/move/${nameOrId.toString().toLowerCase()}`);
    return response.data;
  }

  /**
   * Search for Pokémon by partial name match
   * @param query The search query
   * @param limit Maximum number of results to return
   * @returns A list of Pokémon matching the query
   */
  async searchPokemon(query: string, limit: number = 10): Promise<PokemonListResponse> {
    // Get a list of all Pokémon (limited to 2000 for practical purposes)
    const response = await this.client.get<PokemonListResponse>('/pokemon', {
      params: {
        limit: 2000
      }
    });
    
    // Filter results by name matching the query
    const filteredResults = response.data.results.filter(
      pokemon => pokemon.name.includes(query.toLowerCase())
    ).slice(0, limit);
    
    return {
      ...response.data,
      count: filteredResults.length,
      results: filteredResults
    };
  }

  /**
   * Get resource by URL
   * @param url The full URL of the resource
   * @returns The resource data
   */
  async getByUrl<T>(url: string): Promise<T> {
    const response = await axios.get<T>(url);
    return response.data;
  }
}

// Create and export a singleton instance of the PokéAPI client
export const pokeApiClient = new PokeApiClient();
