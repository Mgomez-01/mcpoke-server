/**
 * Utilities for managing Pokémon images and sprites
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import axios from 'axios';

// Get the current directory when using ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Calculate base paths
const PROJECT_ROOT = path.resolve(__dirname, '../../../');
const ASSETS_DIR = path.join(PROJECT_ROOT, 'assets');
const SPRITES_DIR = path.join(ASSETS_DIR, 'sprites');
const ARTWORK_DIR = path.join(ASSETS_DIR, 'artwork');

// Ensure directories exist
function ensureDirectoriesExist(): void {
  const dirs = [
    ASSETS_DIR,
    SPRITES_DIR,
    path.join(SPRITES_DIR, 'pokemon'),
    path.join(SPRITES_DIR, 'pokemon/shiny'),
    ARTWORK_DIR
  ];
  
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
}

/**
 * Download an image and save it locally
 * @param url The URL of the image to download
 * @param savePath The local path to save the image to
 * @returns The local path to the saved image, or null if download failed
 */
async function downloadImage(url: string | null, savePath: string): Promise<string | null> {
  // If URL is null, return null
  if (!url) return null;
  
  try {
    // Check if file already exists
    if (fs.existsSync(savePath)) {
      return savePath;
    }
    
    // Download the image
    const response = await axios.get(url, { responseType: 'arraybuffer' });
    
    // Ensure the directory exists
    const saveDir = path.dirname(savePath);
    if (!fs.existsSync(saveDir)) {
      fs.mkdirSync(saveDir, { recursive: true });
    }
    
    // Save the image
    fs.writeFileSync(savePath, Buffer.from(response.data, 'binary'));
    
    return savePath;
  } catch (error) {
    console.error(`Failed to download image from ${url}:`, error);
    return null;
  }
}

/**
 * Get the local path for a Pokémon's front default sprite
 * @param id The Pokémon ID
 * @returns The local path to the sprite
 */
function getFrontDefaultSpritePath(id: number): string {
  return path.join(SPRITES_DIR, `pokemon/${id}.png`);
}

/**
 * Get the local path for a Pokémon's front shiny sprite
 * @param id The Pokémon ID
 * @returns The local path to the sprite
 */
function getFrontShinySpritePath(id: number): string {
  return path.join(SPRITES_DIR, `pokemon/shiny/${id}.png`);
}

/**
 * Get the local path for a Pokémon's official artwork
 * @param id The Pokémon ID
 * @returns The local path to the artwork
 */
function getOfficialArtworkPath(id: number): string {
  return path.join(ARTWORK_DIR, `${id}.png`);
}

/**
 * Check if a sprite exists locally
 * @param spritePath The local path to the sprite
 * @returns Whether the sprite exists locally
 */
function spriteExistsLocally(spritePath: string): boolean {
  return fs.existsSync(spritePath);
}

/**
 * Download and cache a Pokémon's sprites
 * @param id The Pokémon ID
 * @param sprites The sprite URLs from the API
 * @returns An object with the local paths to the sprites
 */
async function downloadAndCachePokemonSprites(
  id: number,
  sprites: {
    front_default: string | null;
    front_shiny: string | null;
    official_artwork: string | null;
  }
): Promise<{
  front_default: string | null;
  front_shiny: string | null;
  official_artwork: string | null;
}> {
  // Ensure directories exist
  ensureDirectoriesExist();
  
  // Get local paths
  const frontDefaultPath = getFrontDefaultSpritePath(id);
  const frontShinyPath = getFrontShinySpritePath(id);
  const officialArtworkPath = getOfficialArtworkPath(id);
  
  // Download sprites in parallel
  const [frontDefault, frontShiny, officialArtwork] = await Promise.all([
    downloadImage(sprites.front_default, frontDefaultPath),
    downloadImage(sprites.front_shiny, frontShinyPath),
    downloadImage(sprites.official_artwork, officialArtworkPath)
  ]);
  
  return {
    front_default: frontDefault,
    front_shiny: frontShiny,
    official_artwork: officialArtwork
  };
}

/**
 * Get server URLs for a Pokémon's sprites
 * @param id The Pokémon ID
 * @param baseUrl The base URL of the sprite server (e.g., http://localhost:8080)
 * @returns An object with URLs for the different sprite types
 */
function getPokemonSpriteUrls(id: number, baseUrl: string = 'http://localhost:8080'): {
  front_default: string;
  front_shiny: string;
  official_artwork: string;
} {
  return {
    front_default: `${baseUrl}/sprites/pokemon/${id}.png`,
    front_shiny: `${baseUrl}/sprites/pokemon/shiny/${id}.png`,
    official_artwork: `${baseUrl}/artwork/${id}.png`
  };
}

// Export functions
export {
  downloadAndCachePokemonSprites,
  getPokemonSpriteUrls,
  spriteExistsLocally,
  getFrontDefaultSpritePath,
  getFrontShinySpritePath,
  getOfficialArtworkPath
};
