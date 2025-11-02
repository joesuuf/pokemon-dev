import express, { Request, Response } from 'express';
import { spawn } from 'child_process';
import http from 'http';
import path from 'path';

const router = express.Router();

interface StartServerRequest {
  port: number;
  script: string;
}

// Map of scripts to their npm commands
const scriptMap: Record<string, string> = {
  'frontend:4444': 'npm run frontend:4444',
  'dev': 'npm run dev',
  'dev:6666': 'npm run dev:6666',
  'v2:serve': 'npm run v2:serve',
  'carousel:serve': 'npm run carousel:serve',
  'hub': 'npm run hub',
};

// POST /api/start-server - Start a development server
router.post('/start-server', async (req: Request, res: Response) => {
  try {
    const { port, script }: StartServerRequest = req.body;

    if (!port || !script) {
      return res.status(400).json({ 
        error: 'Missing required fields: port and script' 
      });
    }

    const command = scriptMap[script];
    if (!command) {
      return res.status(400).json({ 
        error: `Unknown script: ${script}` 
      });
    }

    // Get the project root directory
    const projectRoot = path.resolve(__dirname, '../..');

    // Start the server process
    const [cmd, ...args] = command.split(' ');
    const childProcess = spawn(cmd, args, {
      cwd: projectRoot,
      detached: true,
      stdio: 'ignore',
      shell: true,
    });

    // Unref so parent process can exit
    childProcess.unref();

    // Wait a moment to see if process starts successfully
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Check if process is still running
    const isRunning = !childProcess.killed && childProcess.exitCode === null;

    if (isRunning) {
      return res.status(200).json({
        success: true,
        message: `Server starting on port ${port}`,
        pid: childProcess.pid,
      });
    } else {
      return res.status(500).json({
        error: 'Failed to start server',
        message: 'Process exited immediately',
      });
    }
  } catch (error) {
    console.error('[Start Server] Error:', error);
    return res.status(500).json({
      error: 'Failed to start server',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

// GET /api/server-status/:port - Check if a server is running
router.get('/server-status/:port', async (req: Request, res: Response) => {
  try {
    const port = parseInt(req.params.port, 10);

    if (isNaN(port)) {
      return res.status(400).json({ error: 'Invalid port number' });
    }

    // Try to connect to the server
    const isRunning = await new Promise<boolean>((resolve) => {
      const request = http.request(
        {
          hostname: 'localhost',
          port: port,
          path: '/',
          method: 'HEAD',
          timeout: 2000,
        },
        (response) => {
          resolve(response.statusCode !== undefined);
        }
      );

      request.on('error', () => {
        resolve(false);
      });

      request.on('timeout', () => {
        request.destroy();
        resolve(false);
      });

      request.end();
    });

    return res.status(200).json({
      port,
      isRunning,
    });
  } catch (error) {
    console.error('[Server Status] Error:', error);
    return res.status(500).json({
      error: 'Failed to check server status',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

export default router;
