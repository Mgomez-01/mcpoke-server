# MCPoke Server

A Model Context Protocol (MCP) server that connects to the Pokémon API, enabling AI assistants to access comprehensive Pokémon information.

![MCPoke Server Banner](https://raw.githubusercontent.com/username/mcpoke-server/main/assets/banner.png)

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

Response:
```json
{
  "id": 25,
  "name": "Pikachu",
  "types": ["electric"],
  "height": 0.4,
  "weight": 6.0,
  "abilities": [
    {
      "name": "Static",
      "is_hidden": false
    },
    {
      "name": "Lightning Rod",
      "is_hidden": true
    }
  ],
  "stats": {
    "hp": 35,
    "attack": 55,
    "defense": 40,
    "special-attack": 50,
    "special-defense": 50,
    "speed": 90
  },
  "sprites": {
    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/25.png",
    "official_artwork": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
  },
  "description": "When several of these Pokémon gather, their electricity could build and cause lightning storms.",
  "generation": "Generation I",
  "evolution_chain": [
    {
      "name": "Pichu",
      "details": {}
    },
    {
      "name": "Pikachu",
      "details": {
        "method": "Happiness (220+)"
      }
    },
    {
      "name": "Raichu",
      "details": {
        "method": "Use Thunder Stone"
      }
    }
  ]
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

Response:
```json
[
  {
    "id": 4,
    "name": "Charmander",
    "types": ["fire"],
    "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png"
  },
  {
    "id": 5,
    "name": "Charmeleon",
    "types": ["fire"],
    "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/5.png"
  },
  {
    "id": 6,
    "name": "Charizard",
    "types": ["fire", "flying"],
    "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png"
  }
]
```

#### Get Ability Information

```json
{
  "command": "get_ability",
  "name_or_id": "blaze"
}
```

Response:
```json
{
  "id": 66,
  "name": "Blaze",
  "effect": "When this Pokémon has 1/3 or less of its maximum HP, its Fire-type moves inflict 1.5× as much regular damage.",
  "short_effect": "Strengthens Fire moves to inflict 1.5× damage at 1/3 max HP or less.",
  "pokemon": [
    "Charmander",
    "Charmeleon",
    "Charizard",
    "Cyndaquil",
    "Quilava",
    "Typhlosion",
    "Torchic",
    "Combusken",
    "Blaziken",
    "Chimchar",
    "Monferno",
    "Infernape",
    "Tepig",
    "Pignite",
    "Emboar",
    "Fennekin",
    "Braixen",
    "Delphox",
    "Litten",
    "Torracat",
    "Incineroar",
    "Scorbunny",
    "Raboot",
    "Cinderace",
    "Fuecoco",
    "Crocalor",
    "Skeledirge"
  ]
}
```

#### Get Type Information

```json
{
  "command": "get_type",
  "name_or_id": "water"
}
```

Response:
```json
{
  "id": 11,
  "name": "Water",
  "damage_relations": {
    "double_damage_from": [
      "electric",
      "grass"
    ],
    "double_damage_to": [
      "fire",
      "ground",
      "rock"
    ],
    "half_damage_from": [
      "fire",
      "ice",
      "steel",
      "water"
    ],
    "half_damage_to": [
      "dragon",
      "grass",
      "water"
    ],
    "no_damage_from": [],
    "no_damage_to": []
  }
}
```

#### Get Move Information

```json
{
  "command": "get_move",
  "name_or_id": "thunderbolt"
}
```

Response:
```json
{
  "id": 85,
  "name": "Thunderbolt",
  "type": "Electric",
  "power": 90,
  "pp": 15,
  "accuracy": 100,
  "damage_class": "Special",
  "effect": "Inflicts regular damage. Has a 10% chance to paralyze the target.",
  "short_effect": "Has a 10% chance to paralyze the target.",
  "effect_chance": 10
}
```

#### Compare Pokémon

```json
{
  "command": "compare_pokemon",
  "pokemon_list": ["charizard", "blastoise"]
}
```

Response:
```json
{
  "pokemon": [
    {
      "id": 6,
      "name": "Charizard",
      "types": ["fire", "flying"],
      ...
    },
    {
      "id": 9,
      "name": "Blastoise",
      "types": ["water"],
      ...
    }
  ],
  "stat_comparison": {
    "hp": {
      "Charizard": 78,
      "Blastoise": 79
    },
    "attack": {
      "Charizard": 84,
      "Blastoise": 83
    },
    "defense": {
      "Charizard": 78,
      "Blastoise": 100
    },
    "special-attack": {
      "Charizard": 109,
      "Blastoise": 85
    },
    "special-defense": {
      "Charizard": 85,
      "Blastoise": 105
    },
    "speed": {
      "Charizard": 100,
      "Blastoise": 78
    }
  },
  "type_advantages": {
    "Charizard vs Blastoise": {
      "type_effectiveness": {
        "fire": {
          "attacking_type": "Fire",
          "defending_types": ["Water"],
          "effectiveness": 0.5,
          "description": "Not very effective"
        },
        "flying": {
          "attacking_type": "Flying",
          "defending_types": ["Water"],
          "effectiveness": 1.0,
          "description": "Normally effective"
        }
      },
      "average_effectiveness": 0.75,
      "overall_description": "Weak"
    },
    "Blastoise vs Charizard": {
      "type_effectiveness": {
        "water": {
          "attacking_type": "Water",
          "defending_types": ["Fire", "Flying"],
          "effectiveness": 2.0,
          "description": "Super effective"
        }
      },
      "average_effectiveness": 2.0,
      "overall_description": "Strong"
    }
  }
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

Response:
```json
{
  "attacking_type": "Electric",
  "defending_types": ["Water", "Flying"],
  "effectiveness": 4.0,
  "description": "Super effective"
}
```

## Technical Implementation

### Architecture

The MCPoke Server is built with a modular design:

- **Core Server**: Manages MCP protocol handling and request processing
- **API Client**: Handles communication with the PokéAPI
- **Cache Manager**: Optimizes performance through efficient caching
- **Data Processors**: Format and normalize API data for consumption

### Data Flow

1. MCP client (e.g., Claude Desktop) sends a request
2. MCPoke Server processes the request and identifies the required data
3. Server checks its cache for the requested information
4. If not cached, server queries the PokéAPI for the data
5. Server processes and formats the API response
6. Formatted data is returned to the MCP client

### Caching Strategy

To reduce API calls and improve performance, MCPoke Server implements a memory caching system that:

- Stores frequently accessed data in memory
- Caches API responses with configurable TTL (Time To Live)
- Strategically prefetches related data
- Maintains a clean cache purging strategy to prevent memory bloat

## Configuration Options

The server can be configured through a `config.json` file:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": false
  },
  "api": {
    "base_url": "https://pokeapi.co/api/v2",
    "timeout": 10
  },
  "cache": {
    "enabled": true,
    "ttl": 86400,
    "max_size": 1000
  }
}
```

## Project Structure

The MCPoke Server project follows a clean, modular directory structure:

```
mcpoke-server/
├── README.md                 # Project documentation
├── LICENSE                   # MIT license file
├── requirements.txt          # Python dependencies
├── config.example.json       # Example configuration file
├── config.json               # User configuration (gitignored)
├── mcpoke_server.py          # Main server entry point
├── src/
│   ├── __init__.py           # Package initialization
│   ├── server.py             # MCP server implementation
│   ├── api_client.py         # PokéAPI client
│   ├── cache.py              # Caching system
│   ├── processors/
│   │   ├── __init__.py       # Package initialization
│   │   ├── pokemon.py        # Pokémon data processor
│   │   ├── ability.py        # Ability data processor
│   │   ├── move.py           # Move data processor
│   │   └── type.py           # Type data processor
│   └── utils/
│       ├── __init__.py       # Package initialization
│       ├── formatters.py     # Data formatting utilities
│       └── validators.py     # Input validation utilities
├── tests/
│   ├── __init__.py           # Test package initialization
│   ├── test_server.py        # Server tests
│   ├── test_api_client.py    # API client tests
│   ├── test_cache.py         # Cache system tests
│   └── test_processors/      # Data processor tests
│       ├── __init__.py       # Test package initialization
│       ├── test_pokemon.py   # Pokémon processor tests
│       ├── test_ability.py   # Ability processor tests
│       ├── test_move.py      # Move processor tests
│       └── test_type.py      # Type processor tests
├── examples/
│   ├── basic_usage.py        # Basic usage examples
│   ├── advanced_usage.py     # Advanced usage examples
│   └── integration.py        # Integration examples
└── assets/
    ├── banner.png            # Project banner image
    └── icons/                # Icon assets
        ├── type_icons/       # Type icons
        └── stat_icons/       # Stat icons
```

### Key Files and Directories

- **mcpoke_server.py**: The main entry point for the server
- **src/**: Contains all the core implementation code
  - **server.py**: Implements the MCP server protocol
  - **api_client.py**: Handles communication with the PokéAPI
  - **cache.py**: Manages the caching system for improved performance
  - **processors/**: Contains modules for processing different types of data
  - **utils/**: Utility functions and helpers
- **tests/**: Comprehensive test suite
- **examples/**: Usage examples
- **assets/**: Images and other static assets

## Development and Extension

### Adding New Features

MCPoke Server is designed to be easily extensible. To add new features:

1. Create a new method in the `MCPokeServer` class
2. Add the corresponding command handler in the `handle_mcp_request` function
3. Update documentation to reflect the new functionality

### Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Submit a pull request

### Testing

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

## Contact

For issues, suggestions, or contributions, please [open an issue](https://github.com/username/mcpoke-server/issues) on the GitHub repository.

---

Happy Pokémon exploring with your AI assistant!
