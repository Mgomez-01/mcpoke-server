# MCPoke Server

A Model Context Protocol (MCP) server that connects to the Pokémon API, enabling AI assistants to access comprehensive Pokémon information.

## Overview

MCPoke Server provides a bridge between MCP-compatible AI models (like Claude) and the PokéAPI, allowing AI assistants to retrieve and analyze information about Pokémon, moves, abilities, types, and more. This enables rich interactions about the Pokémon universe without needing to switch contexts.

## Features

- 🔍 **Detailed Pokémon Information**: Access comprehensive data for any Pokémon
- 🔎 **Pokémon Search**: Find Pokémon by partial name matches
- ⚔️ **Type Information**: Get type effectiveness and damage relationships
- 💥 **Move Details**: Look up move stats, effects, and properties
- ✨ **Ability Information**: Get ability descriptions and Pokémon that have them
- 📊 **Pokémon Comparison**: Compare multiple Pokémon side by side
- 🧮 **Type Effectiveness Calculator**: Calculate type matchups for battles
- 🧠 **Memory Caching**: Efficient request caching to reduce API calls

## Installation

### Prerequisites

- Node.js 16+
- npm or yarn package manager

### Installation Steps

1. Clone the repository
   ```bash
   git clone https://github.com/username/mcpoke-server.git
   cd mcpoke-server
   ```

2. Install dependencies
   ```bash
   npm install
   ```

3. Configure the server (optional)
   ```bash
   cp config.example.json config.json
   # Edit config.json with your preferred settings
   ```

4. Build and start the server
   ```bash
   npm run build
   npm start
   ```

## Usage with MCP Clients

MCPoke Server can be used with any MCP-compatible client, such as Claude Desktop, to access Pokémon information.

### Example Commands

#### Get Information About a Pokémon

```json
{
  "command": "get_pokemon",
  "name_or_id": "pikachu"
}
```

#### Search for Pokémon

```json
{
  "command": "search_pokemon",
  "query": "char",
  "limit": 3
}
```

#### Get Ability Information

```json
{
  "command": "get_ability",
  "name_or_id": "blaze"
}
```

#### Get Type Information

```json
{
  "command": "get_type",
  "name_or_id": "water"
}
```

#### Get Move Information

```json
{
  "command": "get_move",
  "name_or_id": "thunderbolt"
}
```

#### Compare Pokémon

```json
{
  "command": "compare_pokemon",
  "pokemon_list": ["charizard", "blastoise"]
}
```

#### Calculate Type Effectiveness

```json
{
  "command": "get_type_effectiveness",
  "attacking_type": "electric",
  "defending_types": ["water", "flying"]
}
```

## Testing with MCP Inspector

The MCP Inspector tool can be used to test the server during development:

```bash
# Install the MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run the MCP Inspector with our server
npx @modelcontextprotocol/inspector npm start
```

## Configuration for Claude Desktop

To use the MCPoke Server with Claude Desktop, users need to configure their Claude Desktop app:

```json
{
  "mcpServers": {
    "mcpoke-server": {
      "command": "npx",
      "args": ["mcpoke-server"],
      "env": {}
    }
  }
}
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- [PokéAPI](https://pokeapi.co/) for providing the comprehensive Pokémon data API
- The Model Context Protocol (MCP) community for developing the protocol standard
- All Pokémon content and images are the intellectual property of Nintendo, Game Freak, and The Pokémon Company
