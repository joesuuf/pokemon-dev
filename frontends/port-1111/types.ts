export interface ServerConfig {
  port: number;
  name: string;
  startScript: string;
  type: string;
  description: string;
  techStack: string[];
  accentColor: string;
  accentLight: string;
}

export interface ServerStatus {
  port: number;
  isRunning: boolean;
  name: string;
}

export interface StartServerResponse {
  success: boolean;
  message: string;
  pid?: number;
  killedExisting?: number;
}

export interface KillServerResponse {
  success: boolean;
  message: string;
  killed: number;
  pids?: number[];
}
