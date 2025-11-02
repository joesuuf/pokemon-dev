// src/config/apiConfig.ts
/**
 * API Configuration
 * Controls which API mode to use: direct API calls or masterlist-based search
 * Supports runtime switching via toggle
 */

export type ApiMode = 'direct' | 'masterlist';

// Runtime API mode state (can be changed via toggle)
let currentApiMode: ApiMode | null = null;

/**
 * Get the initial API mode from environment variable or default
 */
function getInitialApiMode(): ApiMode {
  const envMode = import.meta.env.VITE_API_MODE;
  if (envMode === 'direct' || envMode === 'masterlist') {
    return envMode;
  }
  // Default to masterlist for better performance
  return 'masterlist';
}

/**
 * Get the current API mode (runtime or initial)
 */
export function getApiMode(): ApiMode {
  if (currentApiMode !== null) {
    return currentApiMode;
  }
  return getInitialApiMode();
}

/**
 * Set the API mode at runtime
 */
export function setApiMode(mode: ApiMode): void {
  currentApiMode = mode;
  console.log(`[API CONFIG] API mode changed to: ${mode}`);
}

/**
 * Check if we should use direct API calls
 */
export function useDirectApi(): boolean {
  return getApiMode() === 'direct';
}

/**
 * Check if we should use masterlist-based search
 */
export function useMasterlistApi(): boolean {
  return getApiMode() === 'masterlist';
}
