// src/components/ApiToggle.tsx
import React from 'react';
import { ApiMode, getApiMode, setApiMode } from '../config/apiConfig';

interface ApiToggleProps {
  onModeChange?: (mode: ApiMode) => void;
}

export const ApiToggle: React.FC<ApiToggleProps> = ({ onModeChange }) => {
  const [currentMode, setCurrentMode] = React.useState<ApiMode>(getApiMode());

  const handleToggle = (newMode: ApiMode) => {
    if (newMode !== currentMode) {
      setApiMode(newMode);
      setCurrentMode(newMode);
      if (onModeChange) {
        onModeChange(newMode);
      }
      console.log(`[API TOGGLE] Switched to ${newMode} mode`);
    }
  };

  return (
    <div className="api-toggle-container">
      <div className="api-toggle-label">API Mode:</div>
      <div className="api-toggle-switch">
        <button
          className={`api-toggle-button ${currentMode === 'masterlist' ? 'active' : ''}`}
          onClick={() => handleToggle('masterlist')}
          title="Use cached masterlist for faster searches"
        >
          📦 Masterlist
        </button>
        <button
          className={`api-toggle-button ${currentMode === 'direct' ? 'active' : ''}`}
          onClick={() => handleToggle('direct')}
          title="Use direct API calls for real-time results"
        >
          🔗 Direct API
        </button>
      </div>
    </div>
  );
};
