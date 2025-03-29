/**
 * Utility script to clear sprite cache
 * 
 * This can be run directly with:
 * node build/utils/images/clear-cache.js [--all|--regular|--shiny|--artwork]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the current directory when using ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Calculate base paths
const PROJECT_ROOT = path.resolve(__dirname, '../../../');
const ASSETS_DIR = path.join(PROJECT_ROOT, 'assets');
const SPRITES_DIR = path.join(ASSETS_DIR, 'sprites');
const POKEMON_SPRITES_DIR = path.join(SPRITES_DIR, 'pokemon');
const SHINY_SPRITES_DIR = path.join(POKEMON_SPRITES_DIR, 'shiny');
const ARTWORK_DIR = path.join(ASSETS_DIR, 'artwork');

/**
 * Clear all sprite files from the cache
 * @param clearRegular Whether to clear regular sprites
 * @param clearShiny Whether to clear shiny sprites
 * @param clearArtwork Whether to clear official artwork
 */
function clearSpriteCache(
  clearRegular: boolean = true,
  clearShiny: boolean = true,
  clearArtwork: boolean = true
): void {
  console.log('Clearing sprite cache...');

  let count = 0;

  // Clear regular sprites
  if (clearRegular && fs.existsSync(POKEMON_SPRITES_DIR)) {
    const files = fs.readdirSync(POKEMON_SPRITES_DIR)
      .filter(file => file.endsWith('.png') && !file.includes('shiny'));
    
    for (const file of files) {
      fs.unlinkSync(path.join(POKEMON_SPRITES_DIR, file));
      count++;
    }
    console.log(`Cleared ${files.length} regular sprites.`);
  }

  // Clear shiny sprites
  if (clearShiny && fs.existsSync(SHINY_SPRITES_DIR)) {
    const files = fs.readdirSync(SHINY_SPRITES_DIR)
      .filter(file => file.endsWith('.png'));
    
    for (const file of files) {
      fs.unlinkSync(path.join(SHINY_SPRITES_DIR, file));
      count++;
    }
    console.log(`Cleared ${files.length} shiny sprites.`);
  }

  // Clear official artwork
  if (clearArtwork && fs.existsSync(ARTWORK_DIR)) {
    const files = fs.readdirSync(ARTWORK_DIR)
      .filter(file => file.endsWith('.png'));
    
    for (const file of files) {
      fs.unlinkSync(path.join(ARTWORK_DIR, file));
      count++;
    }
    console.log(`Cleared ${files.length} official artwork.`);
  }

  console.log(`Sprite cache cleared. Removed ${count} total files.`);
}

// If called directly
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  
  if (args.includes('--help')) {
    console.log(`
    Usage: node clear-cache.js [OPTIONS]
    
    Options:
      --all      Clear all sprites (default)
      --regular  Clear only regular sprites
      --shiny    Clear only shiny sprites
      --artwork  Clear only official artwork
      --help     Show this help message
    `);
    process.exit(0);
  }
  
  if (args.length === 0 || args.includes('--all')) {
    clearSpriteCache(true, true, true);
  } else {
    clearSpriteCache(
      args.includes('--regular'),
      args.includes('--shiny'),
      args.includes('--artwork')
    );
  }
}

export { clearSpriteCache };
