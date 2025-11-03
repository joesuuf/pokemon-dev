import { useState } from 'react';
import { ServerConfig } from '../types';
import { getServerUrlForPort } from '../services/api';
import './ServerCard.css';

interface ServerCardProps {
  server: ServerConfig;
  // Removed: isRunning, isChecking, onAction
}

export function ServerCard({ server }: ServerCardProps) {
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

      {/* Removed: status and action buttons */}
      <div className="server-actions">
        <a
          href={serverUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="action-button"
          style={{ background: server.accentColor }}
        >
          Open Server →
        </a>
      </div>
    </div>
  );
}
