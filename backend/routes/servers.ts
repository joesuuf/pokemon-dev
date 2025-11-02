import express, { Request, Response } from 'express';
import { spawn, exec } from 'child_process';
import http from 'http';
import path from 'path';
import { promisify } from 'util';
import os from 'os';

const router = express.Router();
const execAsync = promisify(exec);

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

// Helper function to find processes on a port
async function findProcessesOnPort(port: number): Promise<number[]> {
  const pids: number[] = [];
  const platform = os.platform();

  try {
    if (platform === 'linux' || platform === 'darwin') {
      // Use lsof for Linux/Mac
      const { stdout } = await execAsync(`lsof -ti :${port}`);
      if (stdout.trim()) {
        const pidStrings = stdout.trim().split('\n');
        for (const pidStr of pidStrings) {
          const pid = parseInt(pidStr, 10);
          if (!isNaN(pid)) {
            pids.push(pid);
          }
        }
      }
    } else if (platform === 'win32') {
      // Use netstat for Windows
      const { stdout } = await execAsync(`netstat -ano | findstr :${port}`);
      const lines = stdout.split('\n');
      for (const line of lines) {
        if (line.includes('LISTENING')) {
          const parts = line.trim().split(/\s+/);
          if (parts.length > 0) {
            const pidStr = parts[parts.length - 1];
            const pid = parseInt(pidStr, 10);
            if (!isNaN(pid)) {
              pids.push(pid);
            }
          }
        }
      }
    }
  } catch (error) {
    // No processes found or command failed - that's okay
    console.log(`[Kill Server] No processes found on port ${port}`);
  }

  return pids;
}

// Helper function to kill a process
async function killProcess(pid: number, force: boolean = false): Promise<boolean> {
  const platform = os.platform();

  try {
    if (platform === 'win32') {
      const signal = force ? '/F' : '';
      await execAsync(`taskkill /PID ${pid} ${signal} /T`);
    } else {
      const signal = force ? 'KILL' : 'TERM';
      await execAsync(`kill -${signal} ${pid}`);
    }
    return true;
  } catch (error) {
    console.error(`[Kill Server] Error killing PID ${pid}:`, error);
    return false;
  }
}

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

    // Kill any existing processes on this port first
    const existingPids = await findProcessesOnPort(port);
    if (existingPids.length > 0) {
      console.log(`[Start Server] Killing ${existingPids.length} existing process(es) on port ${port}`);
      
      // Try graceful shutdown first
      for (const pid of existingPids) {
        await killProcess(pid, false);
      }

      // Wait for graceful shutdown
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Force kill any remaining processes
      const remainingPids = await findProcessesOnPort(port);
      for (const pid of remainingPids) {
        await killProcess(pid, true);
      }

      // Wait a bit more for ports to fully release
      await new Promise(resolve => setTimeout(resolve, 500));
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
        killedExisting: existingPids.length,
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

// POST /api/kill-server/:port - Kill all processes on a port
router.post('/kill-server/:port', async (req: Request, res: Response) => {
  try {
    const port = parseInt(req.params.port, 10);

    if (isNaN(port)) {
      return res.status(400).json({ error: 'Invalid port number' });
    }

    // Find all processes on the port
    const pids = await findProcessesOnPort(port);

    if (pids.length === 0) {
      return res.status(200).json({
        success: true,
        message: `No processes found on port ${port}`,
        killed: 0,
      });
    }

    // Try graceful shutdown first
    let killed = 0;
    for (const pid of pids) {
      if (await killProcess(pid, false)) {
        killed++;
      }
    }

    // Wait a moment for graceful shutdown
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Force kill any remaining processes
    const remainingPids = await findProcessesOnPort(port);
    for (const pid of remainingPids) {
      if (await killProcess(pid, true)) {
        killed++;
      }
    }

    return res.status(200).json({
      success: true,
      message: `Killed ${killed} process(es) on port ${port}`,
      killed,
      pids,
    });
  } catch (error) {
    console.error('[Kill Server] Error:', error);
    return res.status(500).json({
      error: 'Failed to kill server',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

export default router;
