# Working with MCP Text Responses

The MCPoke Server returns all responses as text content (JSON-stringified objects). This matches the MCP protocol requirements. When working with the responses in Claude Desktop, Claude will automatically parse the JSON responses to extract the relevant information.

## Clear Sprite Cache

```json
{
  "method": "call_tool",
  "params": {
    "name": "clear_sprite_cache",
    "arguments": {
      "type": "all"
    }
  }
}
```

## Bulk Download Pokémon Sprites

```json
{
  "method": "call_tool",
  "params": {
    "name": "bulk_download_sprites",
    "arguments": {
      "start_id": 1,
      "end_id": 10,
      "sprite_type": "all"
    }
  }
}
```

## Get Sprite Cache Statistics

```json
{
  "method": "call_tool",
  "params": {
    "name": "get_sprite_cache_stats"
  }
}
```

## Download and Cache Pokémon Sprites

```json
{
  "method": "call_tool",
  "params": {
    "name": "download_sprites",
    "arguments": {
      "name_or_id": "pikachu"
    }
  }
}
```

## Check Sprite Cache Status

```json
{
  "method": "call_tool",
  "params": {
    "name": "check_sprite_cache",
    "arguments": {
      "name_or_id": "pikachu"
    }
  }
}
```

# MCPoke Server Test Examples

Below are example requests you can use to test the MCPoke Server with the MCP Inspector tool.

## Get Pokémon Information

```json
{
  "method": "call_tool",
  "params": {
    "name": "get_pokemon",
    "arguments": {
      "name_or_id": "pikachu"
    }
  }
}
```

## Search for Pokémon

```json
{
  "method": "call_tool",
  "params": {
    "name": "search_pokemon",
    "arguments": {
      "query": "char",
      "limit": 3
    }
  }
}
```

## Get Ability Information

```json
{
  "method": "call_tool",
  "params": {
    "name": "get_ability",
    "arguments": {
      "name_or_id": "static"
    }
  }
}
```

## Get Type Information

```json
{
  "method": "call_tool",
  "params": {
    "name": "get_type",
    "arguments": {
      "name_or_id": "water"
    }
  }
}
```

## Get Move Information

```json
{
  "method": "call_tool",
  "params": {
    "name": "get_move",
    "arguments": {
      "name_or_id": "thunderbolt"
    }
  }
}
```

## Compare Pokémon

```json
{
  "method": "call_tool",
  "params": {
    "name": "compare_pokemon",
    "arguments": {
      "pokemon_list": ["charizard", "blastoise"]
    }
  }
}
```

## Calculate Type Effectiveness

```json
{
  "method": "call_tool",
  "params": {
    "name": "get_type_effectiveness",
    "arguments": {
      "attacking_type": "electric",
      "defending_types": ["water", "flying"]
    }
  }
}
```

## List All Available Tools

```json
{
  "method": "list_tools"
}
```

To use these examples with the MCP Inspector, run:

```bash
cd /home/speedy/repos/playground_claude/mcpoke-server/mcpoke-server
npx @modelcontextprotocol/inspector build/index.js
```

Then, paste any of the example requests into the inspector window when prompted.
