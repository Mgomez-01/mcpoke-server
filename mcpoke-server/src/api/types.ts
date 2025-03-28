/**
 * Type definitions for the PokéAPI responses
 */

export interface PokemonListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: {
    name: string;
    url: string;
  }[];
}

export interface PokemonResponse {
  id: number;
  name: string;
  base_experience: number;
  height: number;
  weight: number;
  abilities: {
    ability: {
      name: string;
      url: string;
    };
    is_hidden: boolean;
    slot: number;
  }[];
  forms: {
    name: string;
    url: string;
  }[];
  game_indices: {
    game_index: number;
    version: {
      name: string;
      url: string;
    };
  }[];
  held_items: {
    item: {
      name: string;
      url: string;
    };
    version_details: {
      rarity: number;
      version: {
        name: string;
        url: string;
      };
    }[];
  }[];
  location_area_encounters: string;
  moves: {
    move: {
      name: string;
      url: string;
    };
    version_group_details: {
      level_learned_at: number;
      move_learn_method: {
        name: string;
        url: string;
      };
      version_group: {
        name: string;
        url: string;
      };
    }[];
  }[];
  species: {
    name: string;
    url: string;
  };
  sprites: {
    back_default: string | null;
    back_female: string | null;
    back_shiny: string | null;
    back_shiny_female: string | null;
    front_default: string | null;
    front_female: string | null;
    front_shiny: string | null;
    front_shiny_female: string | null;
    other: {
      dream_world: {
        front_default: string | null;
        front_female: string | null;
      };
      home: {
        front_default: string | null;
        front_female: string | null;
        front_shiny: string | null;
        front_shiny_female: string | null;
      };
      'official-artwork': {
        front_default: string | null;
        front_shiny: string | null;
      };
    };
  };
  stats: {
    base_stat: number;
    effort: number;
    stat: {
      name: string;
      url: string;
    };
  }[];
  types: {
    slot: number;
    type: {
      name: string;
      url: string;
    };
  }[];
  past_types: {
    generation: {
      name: string;
      url: string;
    };
    types: {
      slot: number;
      type: {
        name: string;
        url: string;
      };
    }[];
  }[];
}

export interface PokemonSpeciesResponse {
  id: number;
  name: string;
  order: number;
  gender_rate: number;
  capture_rate: number;
  base_happiness: number;
  is_baby: boolean;
  is_legendary: boolean;
  is_mythical: boolean;
  hatch_counter: number;
  has_gender_differences: boolean;
  forms_switchable: boolean;
  growth_rate: {
    name: string;
    url: string;
  };
  pokedex_numbers: {
    entry_number: number;
    pokedex: {
      name: string;
      url: string;
    };
  }[];
  egg_groups: {
    name: string;
    url: string;
  }[];
  color: {
    name: string;
    url: string;
  };
  shape: {
    name: string;
    url: string;
  };
  evolves_from_species: {
    name: string;
    url: string;
  } | null;
  evolution_chain: {
    url: string;
  };
  habitat: {
    name: string;
    url: string;
  } | null;
  generation: {
    name: string;
    url: string;
  };
  names: {
    name: string;
    language: {
      name: string;
      url: string;
    };
  }[];
  flavor_text_entries: {
    flavor_text: string;
    language: {
      name: string;
      url: string;
    };
    version: {
      name: string;
      url: string;
    };
  }[];
  form_descriptions: {
    description: string;
    language: {
      name: string;
      url: string;
    };
  }[];
  genera: {
    genus: string;
    language: {
      name: string;
      url: string;
    };
  }[];
  varieties: {
    is_default: boolean;
    pokemon: {
      name: string;
      url: string;
    };
  }[];
}

export interface EvolutionChainResponse {
  id: number;
  baby_trigger_item: {
    name: string;
    url: string;
  } | null;
  chain: {
    is_baby: boolean;
    species: {
      name: string;
      url: string;
    };
    evolution_details: null | {
      item: {
        name: string;
        url: string;
      } | null;
      trigger: {
        name: string;
        url: string;
      } | null;
      gender: number | null;
      held_item: {
        name: string;
        url: string;
      } | null;
      known_move: {
        name: string;
        url: string;
      } | null;
      known_move_type: {
        name: string;
        url: string;
      } | null;
      location: {
        name: string;
        url: string;
      } | null;
      min_level: number | null;
      min_happiness: number | null;
      min_beauty: number | null;
      min_affection: number | null;
      needs_overworld_rain: boolean;
      party_species: {
        name: string;
        url: string;
      } | null;
      party_type: {
        name: string;
        url: string;
      } | null;
      relative_physical_stats: number | null;
      time_of_day: string;
      trade_species: {
        name: string;
        url: string;
      } | null;
      turn_upside_down: boolean;
    }[];
    evolves_to: {
      is_baby: boolean;
      species: {
        name: string;
        url: string;
      };
      evolution_details: {
        item: {
          name: string;
          url: string;
        } | null;
        trigger: {
          name: string;
          url: string;
        };
        gender: number | null;
        held_item: {
          name: string;
          url: string;
        } | null;
        known_move: {
          name: string;
          url: string;
        } | null;
        known_move_type: {
          name: string;
          url: string;
        } | null;
        location: {
          name: string;
          url: string;
        } | null;
        min_level: number | null;
        min_happiness: number | null;
        min_beauty: number | null;
        min_affection: number | null;
        needs_overworld_rain: boolean;
        party_species: {
          name: string;
          url: string;
        } | null;
        party_type: {
          name: string;
          url: string;
        } | null;
        relative_physical_stats: number | null;
        time_of_day: string;
        trade_species: {
          name: string;
          url: string;
        } | null;
        turn_upside_down: boolean;
      }[];
      evolves_to: {
        is_baby: boolean;
        species: {
          name: string;
          url: string;
        };
        evolution_details: {
          item: {
            name: string;
            url: string;
          } | null;
          trigger: {
            name: string;
            url: string;
          };
          gender: number | null;
          held_item: {
            name: string;
            url: string;
          } | null;
          known_move: {
            name: string;
            url: string;
          } | null;
          known_move_type: {
            name: string;
            url: string;
          } | null;
          location: {
            name: string;
            url: string;
          } | null;
          min_level: number | null;
          min_happiness: number | null;
          min_beauty: number | null;
          min_affection: number | null;
          needs_overworld_rain: boolean;
          party_species: {
            name: string;
            url: string;
          } | null;
          party_type: {
            name: string;
            url: string;
          } | null;
          relative_physical_stats: number | null;
          time_of_day: string;
          trade_species: {
            name: string;
            url: string;
          } | null;
          turn_upside_down: boolean;
        }[];
        evolves_to: any[];
      }[];
    }[];
  };
}

export interface AbilityResponse {
  id: number;
  name: string;
  is_main_series: boolean;
  generation: {
    name: string;
    url: string;
  };
  names: {
    name: string;
    language: {
      name: string;
      url: string;
    };
  }[];
  effect_entries: {
    effect: string;
    short_effect: string;
    language: {
      name: string;
      url: string;
    };
  }[];
  effect_changes: {
    version_group: {
      name: string;
      url: string;
    };
    effect_entries: {
      effect: string;
      language: {
        name: string;
        url: string;
      };
    }[];
  }[];
  flavor_text_entries: {
    flavor_text: string;
    language: {
      name: string;
      url: string;
    };
    version_group: {
      name: string;
      url: string;
    };
  }[];
  pokemon: {
    is_hidden: boolean;
    slot: number;
    pokemon: {
      name: string;
      url: string;
    };
  }[];
}

export interface TypeResponse {
  id: number;
  name: string;
  damage_relations: {
    no_damage_to: {
      name: string;
      url: string;
    }[];
    half_damage_to: {
      name: string;
      url: string;
    }[];
    double_damage_to: {
      name: string;
      url: string;
    }[];
    no_damage_from: {
      name: string;
      url: string;
    }[];
    half_damage_from: {
      name: string;
      url: string;
    }[];
    double_damage_from: {
      name: string;
      url: string;
    }[];
  };
  past_damage_relations: {
    generation: {
      name: string;
      url: string;
    };
    damage_relations: {
      no_damage_to: {
        name: string;
        url: string;
      }[];
      half_damage_to: {
        name: string;
        url: string;
      }[];
      double_damage_to: {
        name: string;
        url: string;
      }[];
      no_damage_from: {
        name: string;
        url: string;
      }[];
      half_damage_from: {
        name: string;
        url: string;
      }[];
      double_damage_from: {
        name: string;
        url: string;
      }[];
    };
  }[];
  game_indices: {
    game_index: number;
    generation: {
      name: string;
      url: string;
    };
  }[];
  generation: {
    name: string;
    url: string;
  };
  move_damage_class: {
    name: string;
    url: string;
  };
  names: {
    name: string;
    language: {
      name: string;
      url: string;
    };
  }[];
  pokemon: {
    slot: number;
    pokemon: {
      name: string;
      url: string;
    };
  }[];
  moves: {
    name: string;
    url: string;
  }[];
}

export interface MoveResponse {
  id: number;
  name: string;
  accuracy: number | null;
  effect_chance: number | null;
  pp: number | null;
  priority: number;
  power: number | null;
  contest_combos: {
    normal: {
      use_before: {
        name: string;
        url: string;
      }[] | null;
      use_after: {
        name: string;
        url: string;
      }[] | null;
    } | null;
    super: {
      use_before: {
        name: string;
        url: string;
      }[] | null;
      use_after: {
        name: string;
        url: string;
      }[] | null;
    } | null;
  } | null;
  contest_type: {
    name: string;
    url: string;
  } | null;
  contest_effect: {
    url: string;
  } | null;
  damage_class: {
    name: string;
    url: string;
  } | null;
  effect_entries: {
    effect: string;
    short_effect: string;
    language: {
      name: string;
      url: string;
    };
  }[];
  effect_changes: {
    version_group: {
      name: string;
      url: string;
    };
    effect_entries: {
      effect: string;
      language: {
        name: string;
        url: string;
      };
    }[];
  }[];
  flavor_text_entries: {
    flavor_text: string;
    language: {
      name: string;
      url: string;
    };
    version_group: {
      name: string;
      url: string;
    };
  }[];
  generation: {
    name: string;
    url: string;
  };
  machines: {
    machine: {
      url: string;
    };
    version_group: {
      name: string;
      url: string;
    };
  }[];
  meta: {
    ailment: {
      name: string;
      url: string;
    };
    ailment_chance: number;
    category: {
      name: string;
      url: string;
    };
    crit_rate: number;
    drain: number;
    flinch_chance: number;
    healing: number;
    max_hits: number | null;
    max_turns: number | null;
    min_hits: number | null;
    min_turns: number | null;
    stat_chance: number;
  } | null;
  names: {
    name: string;
    language: {
      name: string;
      url: string;
    };
  }[];
  past_values: {
    accuracy: number | null;
    effect_chance: number | null;
    power: number | null;
    pp: number | null;
    effect_entries: {
      effect: string;
      short_effect: string;
      language: {
        name: string;
        url: string;
      };
    }[];
    type: {
      name: string;
      url: string;
    } | null;
    version_group: {
      name: string;
      url: string;
    };
  }[];
  stat_changes: {
    change: number;
    stat: {
      name: string;
      url: string;
    };
  }[];
  super_contest_effect: {
    url: string;
  } | null;
  target: {
    name: string;
    url: string;
  };
  type: {
    name: string;
    url: string;
  };
}
