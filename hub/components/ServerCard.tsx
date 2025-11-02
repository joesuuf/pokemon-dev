import { useState } from 'react';
import { ServerConfig } from '../types';
import { startServer, killServer, getServerUrlForPort } from '../services/api';
import './ServerCard.css';

interface ServerCardProps {
  server: ServerConfig;
  isRunning: boolean;
  isChecking: boolean;
  onAction: () => void;
}

export function ServerCard({ server, isRunning, isChecking, onAction }: ServerCardProps) {
  const [isActioning, setIsActioning] = useState(false);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const handleStart = async () => {
    setIsActioning(true);
    setActionMessage(null);
    
    try {
      const result = await startServer(server.port, server.startScript);
      setActionMessage(
        result.killedExisting && result.killedExisting > 0
          ? `Starting... (killed ${result.killedExisting} existing process(es))`
          : 'Starting server...'
      );
      
      // Wait a bit then refresh status
      setTimeout(() => {
        onAction();
        setIsActioning(false);
        setActionMessage(null);
      }, 3000);
    } catch (error) {
      setActionMessage(error instanceof Error ? error.message : 'Failed to start server');
      setIsActioning(false);
    }
  };

  const handleKill = async () => {
    setIsActioning(true);
    setActionMessage(null);
    
    try {
      const result = await killServer(server.port);
      setActionMessage(`Killed ${result.killed} process(es)`);
      
      // Refresh status immediately
      setTimeout(() => {
        onAction();
        setIsActioning(false);
        setActionMessage(null);
      }, 1000);
    } catch (error) {
      setActionMessage(error instanceof Error ? error.message : 'Failed to kill server');
      setIsActioning(false);
    }
  };

  const serverUrl = getServerUrlForPort(server.port);

  return (
    <div className="server-card" style={{ '--accent-color': server.accentColor, '--accent-light': server.accentLight } as React.CSSProperties}>
      <div className="port-badge" style={{ background: server.accentColor }}>
        Port {server.port}
      </div>
      
      <h2>{server.name}</h2>
      <div className="server-type">{server.type}</div>
      
      <p className="description">{server.description}</p>

      <div className="tech-stack">
        {server.techStack.map((tech, index) => (
          <span key={index} className="tech-badge">{tech}</span>
        ))}
      </div>

      <div className="server-status">
        {isChecking ? (
          <div className="status-checking">
            <span className="status-indicator checking"></span>
            Checking...
          </div>
        ) : isRunning ? (
          <div className="status-running">
            <span className="status-indicator active"></span>
            <strong>Running</strong>
          </div>
        ) : (
          <div className="status-stopped">
            <span className="status-indicator inactive"></span>
            <strong>Not Running</strong>
          </div>
        )}
      </div>

      {actionMessage && (
        <div className="action-message">{actionMessage}</div>
      )}

      <div className="server-actions">
        {isRunning ? (
          <>
            <a
              href={serverUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="action-button"
              style={{ background: server.accentColor }}
            >
              Open Server →
            </a>
            <button
              onClick={handleKill}
              disabled={isActioning}
              className="action-button kill-button"
            >
              {isActioning ? 'Killing...' : 'Kill Server'}
            </button>
          </>
        ) : (
          <button
            onClick={handleStart}
            disabled={isActioning}
            className="action-button"
            style={{ background: server.accentColor }}
          >
            {isActioning ? 'Starting...' : 'Start Server'}
          </button>
        )}
      </div>
    </div>
  );
}
