#!/usr/bin/env node

/**
 * MCPoke Server
 * A Model Context Protocol server that provides access to Pokémon data.
 */

import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { server } from './server.js';
import { registerPokemonTools } from './tools/pokemon-tools.js';
import { registerAbilityTools } from './tools/ability-tools.js';
import { registerTypeTools } from './tools/type-tools.js';
import { registerMoveTools } from './tools/move-tools.js';

// Register all tools with the server
registerPokemonTools();
registerAbilityTools();
registerTypeTools();
registerMoveTools();

/**
 * Start the server using stdio transport.
 * This allows the server to communicate via standard input/output streams.
 */
async function main() {
  // Log startup
  console.error('MCPoke Server starting...');
  
  try {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error('MCPoke Server connected.');
  } catch (error) {
    console.error('Error starting MCPoke Server:', error);
    process.exit(1);
  }
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
