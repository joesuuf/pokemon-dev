// src/components/LoadingSpinner.tsx
import React from 'react';
import './LoadingSpinner.css';

interface LoadingSpinnerProps {
  timeRemaining?: number;
}

// PERF-01: Memoize LoadingSpinner component to prevent unnecessary re-renders
const LoadingSpinner = React.memo<LoadingSpinnerProps>(({ timeRemaining = 0 }) => {
  return (
    <div className="loading-container">
      <div className="pokeball-spinner">
        <div className="pokeball">
          <div className="pokeball-top"></div>
          <div className="pokeball-center">
            <div className="pokeball-button">
              <div className="pokeball-timer">{timeRemaining}</div>
            </div>
          </div>
          <div className="pokeball-bottom"></div>
        </div>
      </div>
      <p className="loading-text">Searching for cards... ({timeRemaining}s)</p>
    </div>
  );
});

export default LoadingSpinner;