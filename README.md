# MCPoke Server for Claude Desktop

MCPoke Server is a Model Context Protocol (MCP) server that connects to the Pokémon API, enabling Claude and other AI assistants to access comprehensive Pokémon information. This implementation provides integration with Claude Desktop to enhance conversations about Pokémon.

## Features

- 🔍 **Detailed Pokémon Information**: Get complete data for any Pokémon
- 🔎 **Pokémon Search**: Find Pokémon by name
- ⚔️ **Type Information**: Get type effectiveness and damage relationships
- 💥 **Move Details**: Look up move stats, effects, and properties
- ✨ **Ability Information**: Get ability descriptions and Pokémon that have them
- 📊 **Pokémon Comparison**: Compare multiple Pokémon side by side
- 🧮 **Type Effectiveness Calculator**: Calculate type matchups for battles
- 🧠 **Memory Caching**: Efficient request caching to reduce API calls

## Installation

### Prerequisites

- Node.js 16+
- npm package manager
- Claude Desktop

### Installation Steps

1. Clone the repository
   ```bash
   git clone https://github.com/username/mcpoke-server.git
   cd mcpoke-server
   ```

2. Install dependencies
   ```bash
   cd mcpoke-server
   npm install
   ```

3. Build the server
   ```bash
   npm run build
   ```

## Using with Claude Desktop

### Configuration

To use the MCPoke Server with Claude Desktop, you need to configure your Claude Desktop application:

1. Locate your Claude Desktop configuration file:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Add the following configuration:
   ```json
   {
     "mcpServers": {
       "mcpoke-server": {
         "command": "node",
         "args": ["/path/to/mcpoke-server/mcpoke-server/build/index.js"],
         "env": {}
       }
     }
   }
   ```
   
   Be sure to replace `/path/to/mcpoke-server` with the actual path to the project on your system.

3. Restart Claude Desktop to apply the changes.

### Usage Examples

Once configured, you can ask Claude questions about Pokémon like:

- "Can you tell me about Pikachu's abilities and stats?"
- "What type advantages does Charizard have over Venusaur?"
- "Search for Pokémon with 'eon' in their name"
- "Compare Blastoise and Feraligatr"
- "What does the 'Intimidate' ability do?"
- "Tell me about the move Thunderbolt"
- "How effective is an Electric-type attack against a Water/Flying Pokémon?"

## Testing and Development

### Using the MCP Inspector

You can test the server directly using the MCP Inspector tool:

```bash
cd mcpoke-server
npm run inspector
```

Then use the example requests from the `test_examples.md` file.

### Debugging

For debugging, you can use:

```bash
npm run debug
```

This will start the server with Node.js inspector enabled.

## Acknowledgments

- [PokéAPI](https://pokeapi.co/) for providing the comprehensive Pokémon data
- The Model Context Protocol (MCP) community for developing the protocol standard
- All Pokémon content is the intellectual property of Nintendo, Game Freak, and The Pokémon Company
