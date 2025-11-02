import type { StartServerResponse, KillServerResponse, ServerStatus } from '../types';

const BACKEND_PORT = 3001;

function getBackendUrl(): string {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  return `${protocol}//${hostname}:${BACKEND_PORT}`;
}

function getServerUrl(port: number): string {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  return `${protocol}//${hostname}:${port}`;
}

export async function checkServerStatus(port: number): Promise<boolean> {
  try {
    const backendUrl = getBackendUrl();
    const response = await fetch(`${backendUrl}/api/server-status/${port}`);
    
    if (!response.ok) {
      return false;
    }
    
    const data: ServerStatus = await response.json();
    return data.isRunning;
  } catch (error) {
    console.error(`[API] Error checking server status for port ${port}:`, error);
    return false;
  }
}

export async function startServer(port: number, script: string): Promise<StartServerResponse> {
  try {
    const backendUrl = getBackendUrl();
    const response = await fetch(`${backendUrl}/api/start-server`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ port, script }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'Failed to start server');
    }

    return await response.json();
  } catch (error) {
    console.error('[API] Error starting server:', error);
    throw error;
  }
}

export async function killServer(port: number): Promise<KillServerResponse> {
  try {
    const backendUrl = getBackendUrl();
    const response = await fetch(`${backendUrl}/api/kill-server/${port}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'Failed to kill server');
    }

    return await response.json();
  } catch (error) {
    console.error('[API] Error killing server:', error);
    throw error;
  }
}

export function getServerUrlForPort(port: number): string {
  return getServerUrl(port);
}

export function getHostname(): string {
  return window.location.hostname;
}
