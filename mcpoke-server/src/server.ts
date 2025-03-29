/**
 * MCP server implementation
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

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
  return {
    tools: Object.entries(tools).map(([name, _]) => ({
      name,
      description: getToolDescription(name),
      inputSchema: getToolInputSchema(name)
    }))
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const toolName = request.params.name;
  const handler = tools[toolName];

  if (!handler) {
    throw new Error(`Unknown tool: ${toolName}`);
  }

  try {
    const result = await handler(request.params.arguments || {});
    return {
      content: [{
        type: "text",
        text: JSON.stringify(result)
      }]
    };
  } catch (error: any) {
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
    'get_move': 'Get information about a Pokémon move by name or ID'
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
    }
  };

  return schemas[name] || { type: 'object', properties: {} };
}
