/**
 * Debug utilities for logging and error reporting
 */

// Global flag for debug mode
let debugMode = process.env.DEBUG === 'true';

/**
 * Set debug mode
 * @param enabled Whether debug mode is enabled
 */
export function setDebugMode(enabled: boolean): void {
  debugMode = enabled;
}

/**
 * Log a debug message to the console
 * @param component The component or module that is logging
 * @param message The log message
 * @param data Additional data to log (optional)
 */
export function debugLog(component: string, message: string, data?: any): void {
  if (!debugMode) return;
  
  const timestamp = new Date().toISOString();
  
  if (data !== undefined) {
    console.error(`[${timestamp}] [${component}] ${message}:`, data);
  } else {
    console.error(`[${timestamp}] [${component}] ${message}`);
  }
}

/**
 * Log an error message to the console
 * @param component The component or module that is logging
 * @param error The error object
 * @param message Additional context message (optional)
 */
export function debugError(component: string, error: any, message?: string): void {
  if (!debugMode) return;
  
  const timestamp = new Date().toISOString();
  
  if (message) {
    console.error(`[${timestamp}] [${component}] ERROR - ${message}:`, error);
  } else {
    console.error(`[${timestamp}] [${component}] ERROR:`, error);
  }
}

/**
 * Time a function execution and log the duration
 * @param component The component or module that is timing
 * @param label A label for the timer
 * @param fn The function to time
 * @returns The result of the function
 */
export async function debugTimer<T>(
  component: string, 
  label: string, 
  fn: () => Promise<T> | T
): Promise<T> {
  if (!debugMode) return fn() as Promise<T>;
  
  const start = performance.now();
  
  try {
    const result = await Promise.resolve(fn());
    const duration = performance.now() - start;
    debugLog(component, `${label} completed in ${duration.toFixed(2)}ms`);
    return result;
  } catch (error) {
    const duration = performance.now() - start;
    debugError(component, error, `${label} failed after ${duration.toFixed(2)}ms`);
    throw error;
  }
}

/**
 * Log a warning message to the console
 * @param component The component or module that is logging
 * @param message The warning message
 * @param data Additional data (optional)
 */
export function debugWarn(component: string, message: string, data?: any): void {
  if (!debugMode) return;
  
  const timestamp = new Date().toISOString();
  
  if (data !== undefined) {
    console.error(`[${timestamp}] [${component}] WARNING - ${message}:`, data);
  } else {
    console.error(`[${timestamp}] [${component}] WARNING - ${message}`);
  }
}
