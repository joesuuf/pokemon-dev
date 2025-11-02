// src/config/apiConfig.ts
/**
 * API Configuration
 * Controls which API mode to use: direct API calls or masterlist-based search
 */

export type ApiMode = 'direct' | 'masterlist';

/**
 * Get the current API mode from environment variable or default
 */
export function getApiMode(): ApiMode {
  const envMode = import.meta.env.VITE_API_MODE;
  if (envMode === 'direct' || envMode === 'masterlist') {
    return envMode;
  }
  // Default to masterlist for better performance
  return 'masterlist';
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
