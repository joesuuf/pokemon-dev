// src/components/ErrorMessage.tsx
import React from 'react';
import './ErrorMessage.css';

interface ErrorMessageProps {
  message: string;
}

// PERF-01: Memoize ErrorMessage component to prevent unnecessary re-renders
const ErrorMessage = React.memo<ErrorMessageProps>(({ message }) => {
  return (
    <div className="error-container">
      <div className="error-icon">
        <svg 
          width="60" 
          height="60" 
          viewBox="0 0 24 24" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path 
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" 
            fill="#dc2626"
          />
        </svg>
      </div>
      <h3 className="error-title">Oops! Something went wrong</h3>
      <p className="error-message">{message}</p>
      <div className="error-suggestions">
        <p className="suggestion-title">Try these tips:</p>
        <ul>
          <li>Check your spelling and try again</li>
          <li>Use simpler search terms</li>
          <li>Search for one criteria at a time</li>
          <li>Make sure you're connected to the internet</li>
        </ul>
      </div>
    </div>
  );
});

export default ErrorMessage;