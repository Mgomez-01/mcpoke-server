"""
Tests for the cache manager.
"""

import time
import unittest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cache import CacheManager

class TestCacheManager(unittest.TestCase):
    """Test cases for the cache manager."""
    
    def setUp(self):
        """Set up the test environment."""
        self.cache = CacheManager(
            enabled=True,
            ttl=1,  # 1 second TTL for testing
            max_size=3  # Small max size for testing
        )
    
    def test_get_set(self):
        """Test getting and setting items in the cache."""
        # Set an item in the cache
        self.cache.set("test_key", "test_value")
        
        # Get the item from the cache
        value = self.cache.get("test_key")
        
        # Assert the result
        self.assertEqual(value, "test_value")
    
    def test_get_nonexistent_key(self):
        """Test getting a nonexistent key from the cache."""
        # Get a nonexistent item from the cache
        value = self.cache.get("nonexistent_key")
        
        # Assert the result
        self.assertIsNone(value)
    
    def test_expiration(self):
        """Test that items expire after TTL."""
        # Set an item in the cache
        self.cache.set("test_key", "test_value")
        
        # Wait for the item to expire
        time.sleep(1.1)
        
        # Get the item from the cache
        value = self.cache.get("test_key")
        
        # Assert the result
        self.assertIsNone(value)
    
    def test_cache_size_limit(self):
        """Test that the cache respects the max size limit."""
        # Set more items than the max size
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        self.cache.set("key4", "value4")  # This should cause key1 to be evicted
        
        # Get the items from the cache
        value1 = self.cache.get("key1")
        value2 = self.cache.get("key2")
        value3 = self.cache.get("key3")
        value4 = self.cache.get("key4")
        
        # Assert the results
        self.assertIsNone(value1)
        self.assertEqual(value2, "value2")
        self.assertEqual(value3, "value3")
        self.assertEqual(value4, "value4")
    
    def test_invalidate(self):
        """Test invalidating an item in the cache."""
        # Set an item in the cache
        self.cache.set("test_key", "test_value")
        
        # Invalidate the item
        self.cache.invalidate("test_key")
        
        # Get the item from the cache
        value = self.cache.get("test_key")
        
        # Assert the result
        self.assertIsNone(value)
    
    def test_clear(self):
        """Test clearing the cache."""
        # Set some items in the cache
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        # Clear the cache
        self.cache.clear()
        
        # Get the items from the cache
        value1 = self.cache.get("key1")
        value2 = self.cache.get("key2")
        
        # Assert the results
        self.assertIsNone(value1)
        self.assertIsNone(value2)
    
    def test_cache_disabled(self):
        """Test that the cache doesn't store items when disabled."""
        # Create a disabled cache
        disabled_cache = CacheManager(enabled=False, ttl=60, max_size=100)
        
        # Set an item in the cache
        disabled_cache.set("test_key", "test_value")
        
        # Get the item from the cache
        value = disabled_cache.get("test_key")
        
        # Assert the result
        self.assertIsNone(value)

if __name__ == '__main__':
    unittest.main()
