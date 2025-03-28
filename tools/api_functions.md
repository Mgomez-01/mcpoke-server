# Required API Functions for MCPoke Server

This document lists all the API functions we need to implement for the MCPoke Server.

## get_pokemon

API calls:
- pokemon/{name_or_id}
- pokemon-species/{name_or_id}
- evolution-chain/{id}

## search_pokemon

API calls:
- pokemon?limit={limit}

## get_ability

API calls:
- ability/{name_or_id}

## get_type

API calls:
- type/{name_or_id}

## get_move

API calls:
- move/{name_or_id}

## compare_pokemon

API calls:
- pokemon/{name_or_id} (for each Pokémon in the list)

## get_type_effectiveness

API calls:
- type/{attacking_type}
- type/{defending_type} (for each defending type)


## Summary of Required API Functions

### pokemon

- pokemon/{name_or_id}
- pokemon/{name_or_id} (for each Pokémon in the list)
- pokemon?limit={limit}

### pokemon-species

- pokemon-species/{name_or_id}

### type

- type/{attacking_type}
- type/{defending_type} (for each defending type)
- type/{name_or_id}

### ability

- ability/{name_or_id}

### move

- move/{name_or_id}

### evolution-chain

- evolution-chain/{id}


## Implementation Notes

When implementing the API client, we should:

1. Create a base function for making API requests
2. Create specific functions for each endpoint
3. Implement proper error handling and retries
4. Use the cache to reduce API calls
5. Consider implementing pagination support for list endpoints

## Function Stubs

```python
def make_request(endpoint: str, param: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make a request to the PokéAPI."""
    pass

def fetch_pokemon(name_or_id: str) -> Dict[str, Any]:
    """Fetch Pokémon data."""
    pass

def fetch_pokemon_species(name_or_id: str) -> Dict[str, Any]:
    """Fetch Pokémon species data."""
    pass

def fetch_evolution_chain(chain_id: int) -> Dict[str, Any]:
    """Fetch evolution chain data."""
    pass

def fetch_ability(name_or_id: str) -> Dict[str, Any]:
    """Fetch ability data."""
    pass

def fetch_type(name_or_id: str) -> Dict[str, Any]:
    """Fetch type data."""
    pass

def fetch_move(name_or_id: str) -> Dict[str, Any]:
    """Fetch move data."""
    pass

def fetch_all_pokemon(limit: int = 1000, offset: int = 0) -> Dict[str, Any]:
    """Fetch all Pokémon (paginated)."""
    pass
```
