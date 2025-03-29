/**
 * Cache manager for optimizing API requests
 */
import NodeCache from 'node-cache';
import { debugLog } from '../utils/debug.js';

/**
 * Cache manager for optimizing API requests
 */
class CacheManager {
  private cache: NodeCache;
  private readonly enabled: boolean;

  /**
   * Create a new cache manager
   * @param ttl Time to live in seconds (default: 24 hours)
   * @param maxItems Maximum number of items in the cache
   * @param enabled Whether the cache is enabled
   */
  constructor(ttl: number = 86400, maxItems: number = 1000, enabled: boolean = true) {
    this.enabled = enabled;
    this.cache = new NodeCache({
      stdTTL: ttl, // Time to live in seconds
      maxKeys: maxItems, // Maximum number of items in the cache
      checkperiod: 600, // Check for expired keys every 10 minutes
      useClones: false // Don't clone objects (for performance)
    });
  }

  /**
   * Get a value from the cache
   * @param key The cache key
   * @returns The cached value, or undefined if not found
   */
  get<T>(key: string): T | undefined {
    if (!this.enabled) return undefined;
    
    const value = this.cache.get<T>(key);
    if (value !== undefined) {
      debugLog('Cache', `Cache hit for key: ${key}`);
    } else {
      debugLog('Cache', `Cache miss for key: ${key}`);
    }
    
    return value;
  }

  /**
   * Set a value in the cache
   * @param key The cache key
   * @param value The value to cache
   * @param ttl Time to live in seconds (optional, uses default if not specified)
   * @returns Whether the operation was successful
   */
  set<T>(key: string, value: T, ttl?: number): boolean {
    if (!this.enabled) return false;
    
    // If ttl is undefined, use default TTL (don't pass it to set)
    let result: boolean;
    if (ttl === undefined) {
      result = this.cache.set(key, value);
      debugLog('Cache', `Cached value for key: ${key} with default TTL`);
    } else {
      result = this.cache.set(key, value, ttl);
      debugLog('Cache', `Cached value for key: ${key} with TTL: ${ttl}s`);
    }
    
    return result;
  }

  /**
   * Check if a key exists in the cache
   * @param key The cache key
   * @returns Whether the key exists
   */
  has(key: string): boolean {
    if (!this.enabled) return false;
    return this.cache.has(key);
  }

  /**
   * Delete a value from the cache
   * @param key The cache key
   * @returns Whether the operation was successful
   */
  del(key: string): boolean {
    if (!this.enabled) return false;
    return this.cache.del(key) > 0;
  }

  /**
   * Clear the entire cache
   */
  clear(): void {
    if (!this.enabled) return;
    this.cache.flushAll();
  }

  /**
   * Get or set a value in the cache using a factory function
   * @param key The cache key
   * @param factory A function that returns the value to cache or a Promise that resolves to the value
   * @param ttl Time to live in seconds (optional)
   * @returns The cached value or the result of the factory function
   */
  async getOrSet<T>(key: string, factory: () => Promise<T> | T, ttl?: number): Promise<T> {
    if (!this.enabled) {
      debugLog('Cache', `Cache disabled, directly executing factory for key: ${key}`);
      return Promise.resolve(factory());
    }

    const cachedValue = this.get<T>(key);
    if (cachedValue !== undefined) {
      return cachedValue;
    }

    debugLog('Cache', `Executing factory function for key: ${key}`);
    const value = await Promise.resolve(factory());
    this.set(key, value, ttl);
    return value;
  }
}

// Create and export a singleton instance of the cache manager
export const cacheManager = new CacheManager();
