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

- Python 3.8+
- pip package manager

### Installation Steps

1. Clone the repository
   ```bash
   git clone https://github.com/username/mcpoke-server.git
   cd mcpoke-server
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the server (optional)
   ```bash
   cp config.example.json config.json
   # Edit config.json with your preferred settings
   ```

4. Start the server
   ```bash
   python mcpoke_server.py
   ```

## Usage

Please see the `examples` directory for detailed usage examples. The basic workflow is:

1. Start the MCPoke Server
2. Connect an MCP-compatible client (such as Claude)
3. Send commands to retrieve Pokémon information

## Development

This project is under active development. See the implementation plan in the `implementation_plan_readme.md` file for more details.

### Running Tests

To run the test suite:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [PokéAPI](https://pokeapi.co/) for providing the comprehensive Pokémon data API
- The Model Context Protocol (MCP) community for developing the protocol standard
- All Pokémon content and images are the intellectual property of Nintendo, Game Freak, and The Pokémon Company
