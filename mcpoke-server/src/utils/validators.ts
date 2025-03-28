/**
 * Utility functions for validating data
 */

/**
 * Check if a value is a valid number or numeric string
 * @param value The value to check
 * @returns Whether the value is a valid number
 */
export function isValidNumber(value: any): boolean {
  if (typeof value === 'number') {
    return !isNaN(value);
  }
  
  if (typeof value === 'string') {
    return !isNaN(Number(value)) && value.trim() !== '';
  }
  
  return false;
}

/**
 * Check if a value is a valid Pokémon name or ID
 * @param nameOrId The value to check
 * @returns Whether the value is a valid Pokémon name or ID
 */
export function isValidPokemonNameOrId(nameOrId: any): boolean {
  if (!nameOrId) return false;
  
  // Check if it's a number
  if (isValidNumber(nameOrId)) {
    const num = Number(nameOrId);
    return num > 0 && Number.isInteger(num);
  }
  
  // Check if it's a string
  if (typeof nameOrId === 'string') {
    // Pokemon names should only contain letters, numbers, and hyphens
    return /^[a-zA-Z0-9-]+$/.test(nameOrId.trim());
  }
  
  return false;
}

/**
 * Check if a value is a valid limit
 * @param limit The value to check
 * @returns Whether the value is a valid limit
 */
export function isValidLimit(limit: any): boolean {
  if (!isValidNumber(limit)) return false;
  
  const num = Number(limit);
  return num > 0 && Number.isInteger(num) && num <= 100;
}

/**
 * Validate and sanitize a search query
 * @param query The query to validate
 * @returns The sanitized query, or null if invalid
 */
export function validateSearchQuery(query: any): string | null {
  if (typeof query !== 'string' || query.trim() === '') {
    return null;
  }
  
  // Sanitize the query (remove special characters and whitespace)
  return query.trim().toLowerCase().replace(/[^\w\s-]/g, '');
}

/**
 * Validate a list of Pokémon names or IDs
 * @param list The list to validate
 * @returns Whether the list is valid
 */
export function validatePokemonList(list: any[]): boolean {
  if (!Array.isArray(list) || list.length < 1) {
    return false;
  }
  
  return list.every(item => isValidPokemonNameOrId(item));
}

/**
 * Validate type name
 * @param type The type name to validate
 * @returns Whether the type name is valid
 */
export function isValidTypeName(type: any): boolean {
  if (typeof type !== 'string' || type.trim() === '') {
    return false;
  }
  
  const validTypes = [
    'normal', 'fire', 'water', 'electric', 'grass', 'ice',
    'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug',
    'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy'
  ];
  
  return validTypes.includes(type.toLowerCase());
}
