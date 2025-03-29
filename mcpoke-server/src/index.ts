#!/usr/bin/env node

/**
 * MCPoke Server
 * A Model Context Protocol server that provides access to Pokémon data.
 */

import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { debugLog, debugError } from './utils/debug.js';
import { server } from './server.js';
import { startHttpServer } from './http-server.js';
import { registerPokemonTools } from './tools/pokemon-tools.js';
import { registerAbilityTools } from './tools/ability-tools.js';
import { registerTypeTools } from './tools/type-tools.js';
import { registerMoveTools } from './tools/move-tools.js';
import { registerSpriteTools } from './tools/sprite-tools.js';
import { registerBulkSpriteTools } from './tools/bulk-sprite-tools.js';

// Register all tools with the server
registerPokemonTools();
registerAbilityTools();
registerTypeTools();
registerMoveTools();
registerSpriteTools();
registerBulkSpriteTools();

/**
 * Start the server using stdio transport.
 * This allows the server to communicate via standard input/output streams.
 */
async function main() {
  // Log startup
  console.error('MCPoke Server starting...');
  debugLog('Main', 'MCPoke Server initializing');
  
  // Set up process signal handlers for graceful shutdown
  process.on('SIGINT', handleShutdown);
  process.on('SIGTERM', handleShutdown);
  
  try {
    // Start the HTTP server for serving sprites
    debugLog('Main', 'Starting HTTP server for sprites');
    const httpPort = process.env.HTTP_PORT ? parseInt(process.env.HTTP_PORT) : 8080;
    const httpServer = startHttpServer(httpPort);
    
    debugLog('Main', 'Registering tools completed');
    debugLog('Main', 'Creating StdioServerTransport');
    const transport = new StdioServerTransport();
    
    debugLog('Main', 'Connecting server to transport');
    await server.connect(transport);
    
    console.error('MCPoke Server connected.');
    debugLog('Main', 'MCPoke Server successfully connected and ready');
  } catch (error) {
    debugError('Main', error, 'Error starting MCPoke Server');
    console.error('Error starting MCPoke Server:', error);
    process.exit(1);
  }
}

/**
 * Handle graceful shutdown of the server
 */
function handleShutdown() {
  debugLog('Main', 'Received shutdown signal, closing server');
  console.error('MCPoke Server shutting down...');
  
  // Allow time for cleanup operations (if any were added in the future)
  setTimeout(() => {
    debugLog('Main', 'Server shutdown complete');
    process.exit(0);
  }, 100);
}

main().catch((error) => {
  debugError('Main', error, 'Unhandled error in main process');
  console.error('Server error:', error);
  process.exit(1);
});
