/**
 * MCP server implementation
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { debugLog, debugError } from './utils/debug.js';

// Create an MCP server instance
export const server = new Server(
  {
    name: "MCPoke Server",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define the tools object to store tool handlers
export const tools: Record<string, (args: any) => Promise<any>> = {};

// Set up the request handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  debugLog('Server', 'Received list_tools request');
  const toolsList = Object.entries(tools).map(([name, _]) => ({
    name,
    description: getToolDescription(name),
    inputSchema: getToolInputSchema(name)
  }));
  
  debugLog('Server', `Returning ${toolsList.length} available tools`);
  return { tools: toolsList };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const toolName = request.params.name;
  const args = request.params.arguments || {};
  
  debugLog('Server', `Received call_tool request for ${toolName}`, args);
  
  const handler = tools[toolName];
  if (!handler) {
    debugError('Server', new Error(`Unknown tool: ${toolName}`), 'Tool not found');
    throw new Error(`Unknown tool: ${toolName}`);
  }

  try {
    debugLog('Server', `Executing tool: ${toolName}`);
    const result = await handler(args);
    
    debugLog('Server', `Tool ${toolName} executed successfully`);
    return {
      content: [{
        type: "text",
        text: JSON.stringify(result, null, 2)
      }]
    };
  } catch (error: any) {
    debugError('Server', error, `Error executing tool: ${toolName}`);
    throw new Error(`Tool execution error: ${error.message}`);
  }
});

// Helper functions for tool schemas
function getToolDescription(name: string): string {
  const descriptions: Record<string, string> = {
    'get_pokemon': 'Get detailed information about a Pokémon by name or ID',
    'search_pokemon': 'Search for Pokémon by partial name match',
    'compare_pokemon': 'Compare multiple Pokémon side by side',
    'get_ability': 'Get information about a Pokémon ability by name or ID',
    'get_type': 'Get information about a Pokémon type by name or ID',
    'get_type_effectiveness': 'Calculate type effectiveness between attacking and defending types',
    'get_move': 'Get information about a Pokémon move by name or ID',
    'download_sprites': 'Download and cache all sprites for a Pokémon',
    'check_sprite_cache': 'Check if sprites for a Pokémon are cached locally',
    'bulk_download_sprites': 'Download sprites for a range of Pokémon IDs',
    'get_sprite_cache_stats': 'Get statistics about cached sprites',
    'clear_sprite_cache': 'Clear the sprite cache'
  };

  return descriptions[name] || 'No description available';
}

function getToolInputSchema(name: string): any {
  const schemas: Record<string, any> = {
    'get_pokemon': {
      type: 'object',
      properties: {
        name_or_id: {
          type: 'string',
          description: 'The name or ID of the Pokémon'
        }
      },
      required: ['name_or_id']
    },
    'search_pokemon': {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'The search query'
        },
        limit: {
          type: 'number',
          description: 'Maximum number of results to return (default: 10)'
        }
      },
      required: ['query']
    },
    'compare_pokemon': {
      type: 'object',
      properties: {
        pokemon_list: {
          type: 'array',
          items: {
            type: 'string'
          },
          description: 'List of Pokémon names or IDs to compare'
        }
      },
      required: ['pokemon_list']
    },
    'get_ability': {
      type: 'object',
      properties: {
        name_or_id: {
          type: 'string',
          description: 'The name or ID of the ability'
        }
      },
      required: ['name_or_id']
    },
    'get_type': {
      type: 'object',
      properties: {
        name_or_id: {
          type: 'string',
          description: 'The name or ID of the type'
        }
      },
      required: ['name_or_id']
    },
    'get_type_effectiveness': {
      type: 'object',
      properties: {
        attacking_type: {
          type: 'string',
          description: 'The attacking type'
        },
        defending_types: {
          type: 'array',
          items: {
            type: 'string'
          },
          description: 'The defending types'
        }
      },
      required: ['attacking_type', 'defending_types']
    },
    'get_move': {
      type: 'object',
      properties: {
        name_or_id: {
          type: 'string',
          description: 'The name or ID of the move'
        }
      },
      required: ['name_or_id']
    },
    'download_sprites': {
      type: 'object',
      properties: {
        name_or_id: {
          type: 'string',
          description: 'The name or ID of the Pokémon'
        }
      },
      required: ['name_or_id']
    },
    'check_sprite_cache': {
      type: 'object',
      properties: {
        name_or_id: {
          type: 'string',
          description: 'The name or ID of the Pokémon'
        }
      },
      required: ['name_or_id']
    },
    'bulk_download_sprites': {
      type: 'object',
      properties: {
        start_id: {
          type: 'number',
          description: 'The starting Pokémon ID for the range'
        },
        end_id: {
          type: 'number',
          description: 'The ending Pokémon ID for the range'
        },
        sprite_type: {
          type: 'string',
          description: 'Type of sprites to download: all, default, shiny, or artwork (default: all)'
        }
      },
      required: ['start_id', 'end_id']
    },
    'get_sprite_cache_stats': {
      type: 'object',
      properties: {}
    },
    'clear_sprite_cache': {
      type: 'object',
      properties: {
        type: {
          type: 'string',
          description: 'Type of sprites to clear: all, regular, shiny, or artwork (default: all)'
        }
      }
    }
  };

  return schemas[name] || { type: 'object', properties: {} };
}
