"""
Cache management system for the MCPoke Server.

This module provides caching functionality to improve performance
and reduce the number of API calls to the PokéAPI.
"""

import logging
import time
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger('mcpoke-server.cache')

class CacheManager:
    """
    Cache manager for the MCPoke Server.
    
    This class provides caching functionality to improve performance
    and reduce the number of API calls to the PokéAPI.
    """
    
    def __init__(self, enabled: bool = True, ttl: int = 86400, max_size: int = 1000):
        """
        Initialize the cache manager.
        
        Args:
            enabled: Whether caching is enabled
            ttl: Time to live (in seconds) for cached items
            max_size: Maximum number of items to keep in the cache
        """
        self.enabled = enabled
        self.ttl = ttl
        self.max_size = max_size
        self.cache: Dict[str, Tuple[float, Any]] = {}
        
        logger.info(f"Cache initialized: enabled={enabled}, ttl={ttl}s, max_size={max_size}")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get an item from the cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached item or None if not found or expired
        """
        if not self.enabled:
            return None
        
        if key not in self.cache:
            return None
        
        timestamp, value = self.cache[key]
        
        if self._is_expired(timestamp):
            logger.debug(f"Cache miss (expired): {key}")
            self.invalidate(key)
            return None
        
        logger.debug(f"Cache hit: {key}")
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set an item in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        if not self.enabled:
            return
        
        # Check if cache is full
        if len(self.cache) >= self.max_size:
            self.prune()
        
        # Store item with current timestamp
        self.cache[key] = (time.time(), value)
        logger.debug(f"Cached: {key}")
    
    def invalidate(self, key: str) -> None:
        """
        Invalidate a cached item.
        
        Args:
            key: Cache key
        """
        if not self.enabled:
            return
        
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Invalidated: {key}")
    
    def clear(self) -> None:
        """Clear the entire cache."""
        if not self.enabled:
            return
        
        self.cache.clear()
        logger.debug("Cache cleared")
    
    def prune(self) -> None:
        """
        Prune expired items from the cache.
        
        This method is called automatically when the cache gets too large.
        """
        if not self.enabled:
            return
        
        # First, remove expired items
        expired_keys = [
            key for key, (timestamp, _) in self.cache.items()
            if self._is_expired(timestamp)
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        # If still too large, remove oldest items
        if len(self.cache) >= self.max_size:
            # Sort by timestamp (oldest first)
            sorted_items = sorted(self.cache.items(), key=lambda x: x[1][0])
            
            # Number of items to remove
            num_to_remove = len(self.cache) - self.max_size + 10  # Remove extra to avoid frequent pruning
            
            # Remove oldest items
            for key, _ in sorted_items[:num_to_remove]:
                del self.cache[key]
        
        logger.debug(f"Pruned {len(expired_keys)} expired items, cache size: {len(self.cache)}")
    
    def _is_expired(self, timestamp: float) -> bool:
        """
        Check if a cached item is expired.
        
        Args:
            timestamp: Timestamp when the item was cached
        
        Returns:
            True if the item is expired, False otherwise
        """
        return time.time() - timestamp > self.ttl
