/**
 * Configuration utility for the server
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Get the current directory when using ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Configuration interface
 */
export interface Config {
  server: {
    host: string;
    port: number;
    debug: boolean;
  };
  api: {
    base_url: string;
    timeout: number;
  };
  cache: {
    enabled: boolean;
    ttl: number;
    max_size: number;
  };
}

/**
 * Default configuration
 */
const defaultConfig: Config = {
  server: {
    host: '0.0.0.0',
    port: 8000,
    debug: false
  },
  api: {
    base_url: 'https://pokeapi.co/api/v2',
    timeout: 10
  },
  cache: {
    enabled: true,
    ttl: 86400,
    max_size: 1000
  }
};

/**
 * Load configuration from a JSON file
 * @param configPath Path to the configuration file
 * @returns The loaded configuration
 */
export function loadConfig(configPath?: string): Config {
  // Use default config if no path is provided
  if (!configPath) {
    return defaultConfig;
  }

  try {
    // Read and parse the config file
    const configData = fs.readFileSync(configPath, 'utf-8');
    const userConfig = JSON.parse(configData);

    // Merge with default config
    return {
      server: {
        ...defaultConfig.server,
        ...userConfig.server
      },
      api: {
        ...defaultConfig.api,
        ...userConfig.api
      },
      cache: {
        ...defaultConfig.cache,
        ...userConfig.cache
      }
    };
  } catch (error) {
    console.error(`Error loading config from ${configPath}:`, error);
    return defaultConfig;
  }
}

/**
 * Get the config instance
 */
export const config = loadConfig(
  process.env.CONFIG_PATH || path.join(process.cwd(), 'config.json')
);
