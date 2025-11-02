import { useState, useEffect } from 'react';
import { ServerCard } from './components/ServerCard';
import { ServerConfig } from './types';
import { checkServerStatus, getHostname } from './services/api';
import './App.css';

const SERVER_CONFIGS: ServerConfig[] = [
  {
    port: 4444,
    name: 'OCR Card Search',
    startScript: 'frontend:4444',
    type: 'Google Vision API Integration',
    description: 'Upload an image of a Pokemon card to automatically identify it using Google Cloud Vision API OCR.',
    techStack: ['React 19', 'GCP Vision', 'OCR', 'TypeScript'],
    accentColor: '#06b6d4',
    accentLight: '#22d3ee',
  },
  {
    port: 8888,
    name: 'Main Application',
    startScript: 'dev',
    type: 'Primary Development Server',
    description: 'The core Pokemon TCG Search application running on Vite\'s development server with hot module replacement (HMR).',
    techStack: ['Vite', 'React 19', 'TypeScript', 'TailwindCSS 4'],
    accentColor: '#3b82f6',
    accentLight: '#60a5fa',
  },
  {
    port: 6666,
    name: 'Alternate Dev Server',
    startScript: 'dev:6666',
    type: 'Secondary Development Instance',
    description: 'Identical to the main server but on a different port for multi-instance testing and comparison.',
    techStack: ['Vite', 'React 19', 'Multi-instance'],
    accentColor: '#8b5cf6',
    accentLight: '#a78bfa',
  },
  {
    port: 9999,
    name: 'V2 Application',
    startScript: 'v2:serve',
    type: 'Static Production Build',
    description: 'Production-ready static build served via http-server with advanced security features.',
    techStack: ['http-server', 'Static HTML', 'CORS', 'No Cache'],
    accentColor: '#10b981',
    accentLight: '#34d399',
  },
  {
    port: 7777,
    name: 'Carousel Component',
    startScript: 'carousel:serve',
    type: 'Standalone UI Component',
    description: 'Isolated carousel component demonstration served independently for testing and integration.',
    techStack: ['http-server', 'Standalone', 'Component'],
    accentColor: '#f59e0b',
    accentLight: '#fbbf24',
  },
  {
    port: 1111,
    name: 'Development Hub',
    startScript: 'hub',
    type: 'Central Dashboard (You Are Here)',
    description: 'This page! A central dashboard providing quick access to all running development servers.',
    techStack: ['http-server', 'Dashboard', 'Hub'],
    accentColor: '#ec4899',
    accentLight: '#f472b6',
  },
];

function App() {
  const [serverStatuses, setServerStatuses] = useState<Record<number, boolean>>({});
  const [checkingStatuses, setCheckingStatuses] = useState<Record<number, boolean>>({});
  const [hostname, setHostname] = useState<string>('');

  useEffect(() => {
    setHostname(getHostname());
    updateServerStatuses();
    
    // Refresh status every 10 seconds
    const interval = setInterval(updateServerStatuses, 10000);
    return () => clearInterval(interval);
  }, []);

  const updateServerStatuses = async () => {
    const statusPromises = SERVER_CONFIGS.map(async (server) => {
      setCheckingStatuses(prev => ({ ...prev, [server.port]: true }));
      const isRunning = await checkServerStatus(server.port);
      setCheckingStatuses(prev => ({ ...prev, [server.port]: false }));
      return { port: server.port, isRunning };
    });

    const results = await Promise.all(statusPromises);
    const newStatuses: Record<number, boolean> = {};
    results.forEach(({ port, isRunning }) => {
      newStatuses[port] = isRunning;
    });
    setServerStatuses(newStatuses);
  };

  const handleServerAction = async () => {
    // Refresh statuses after any action
    setTimeout(updateServerStatuses, 2000);
  };

  const allRunning = SERVER_CONFIGS.every(server => serverStatuses[server.port] === true);
  const anyRunning = SERVER_CONFIGS.some(server => serverStatuses[server.port] === true);

  return (
    <div className="container">
      <header className="header">
        <h1>🎮 Pokemon TCG Development Hub</h1>
        <p className="subtitle">Central Dashboard for All Development Servers</p>
        <div className="status">
          {allRunning ? (
            <>
              <span className="status-indicator active"></span>
              All Systems Operational{hostname && ` @ ${hostname}`}
            </>
          ) : anyRunning ? (
            <>
              <span className="status-indicator warning"></span>
              Some Servers Running{hostname && ` @ ${hostname}`}
            </>
          ) : (
            <>
              <span className="status-indicator inactive"></span>
              No Servers Running{hostname && ` @ ${hostname}`}
            </>
          )}
        </div>
      </header>

      <div className="servers-grid">
        {SERVER_CONFIGS.map((server) => (
          <ServerCard
            key={server.port}
            server={server}
            isRunning={serverStatuses[server.port] ?? false}
            isChecking={checkingStatuses[server.port] ?? false}
            onAction={handleServerAction}
          />
        ))}
      </div>

      <footer className="footer">
        <p>Pokemon TCG Development Hub • Port 1111</p>
        <p className="footer-version">v2.0.0 • Running on Vite</p>
      </footer>
    </div>
  );
}

export default App;
