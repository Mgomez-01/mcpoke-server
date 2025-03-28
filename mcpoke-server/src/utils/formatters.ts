/**
 * Utility functions for formatting data
 */

/**
 * Capitalize the first letter of a string
 * @param text The string to capitalize
 * @returns The capitalized string
 */
export function capitalizeFirstLetter(text: string): string {
  if (!text || typeof text !== 'string') return '';
  return text.charAt(0).toUpperCase() + text.slice(1);
}

/**
 * Format a number with commas
 * @param num The number to format
 * @returns The formatted number string
 */
export function formatNumber(num: number): string {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Clean a Pokémon description by removing newlines and duplicate spaces
 * @param description The description to clean
 * @returns The cleaned description
 */
export function cleanDescription(description: string): string {
  if (!description) return '';
  
  // Replace newlines and form feeds with spaces
  let cleaned = description.replace(/[\n\f]/g, ' ');
  
  // Replace multiple spaces with a single space
  cleaned = cleaned.replace(/\s+/g, ' ');
  
  return cleaned.trim();
}

/**
 * Format a height value in meters with proper units
 * @param height The height in meters
 * @returns The formatted height string
 */
export function formatHeight(height: number): string {
  return `${height.toFixed(1)}m (${convertMetersToFeetInches(height)})`;
}

/**
 * Format a weight value in kilograms with proper units
 * @param weight The weight in kilograms
 * @returns The formatted weight string
 */
export function formatWeight(weight: number): string {
  const lbs = weight * 2.20462;
  return `${weight.toFixed(1)}kg (${lbs.toFixed(1)} lbs)`;
}

/**
 * Convert meters to feet and inches
 * @param meters The height in meters
 * @returns The height in feet and inches
 */
function convertMetersToFeetInches(meters: number): string {
  const totalInches = meters * 39.3701;
  const feet = Math.floor(totalInches / 12);
  const inches = Math.round(totalInches % 12);
  
  if (inches === 12) {
    return `${feet + 1}'0"`;
  }
  
  return `${feet}'${inches}"`;
}
