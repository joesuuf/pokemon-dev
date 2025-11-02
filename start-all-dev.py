#!/usr/bin/env python3
"""
Start All Dev Servers Script
Kills existing processes on dev ports and starts all servers fresh.
Ports: 1111 (hub), 5555, 6666, 7777, 8888, 9999
"""

import os
import sys
import signal
import subprocess
import platform
import time
from pathlib import Path


# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'  # No Color


# Dev server ports
PORTS = [1111, 5555, 6666, 7777, 8888, 9999]


def print_colored(message: str, color: str = Colors.NC) -> None:
    """Print colored message to terminal."""
    print(f"{color}{message}{Colors.NC}")


def find_processes_on_port(port: int) -> list[int]:
    """Find PIDs of processes using the specified port."""
    pids = []
    system = platform.system()
    
    try:
        if system == "Linux":
            # Using lsof (Linux/Mac)
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                pids = [int(pid) for pid in result.stdout.strip().split('\n') if pid]
        elif system == "Darwin":  # macOS
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                pids = [int(pid) for pid in result.stdout.strip().split('\n') if pid]
        elif system == "Windows":
            # Windows: netstat to find PID
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if f":{port}" in line and "LISTENING" in line:
                        parts = line.split()
                        if parts:
                            pid = parts[-1]
                            try:
                                pids.append(int(pid))
                            except ValueError:
                                pass
    except Exception as e:
        print_colored(f"Warning: Could not check port {port}: {e}", Colors.YELLOW)
    
    return pids


def kill_process(pid: int, force: bool = False) -> bool:
    """Kill a process by PID."""
    try:
        system = platform.system()
        if system == "Windows":
            signal_flag = "/F" if force else ""
            subprocess.run(
                ["taskkill", "/PID", str(pid), signal_flag, "/T"],
                capture_output=True,
                check=False
            )
        else:
            signal_type = signal.SIGKILL if force else signal.SIGTERM
            os.kill(pid, signal_type)
        return True
    except ProcessLookupError:
        # Process already gone
        return False
    except PermissionError:
        print_colored(f"Permission denied killing PID {pid}", Colors.YELLOW)
        return False
    except Exception as e:
        print_colored(f"Error killing PID {pid}: {e}", Colors.YELLOW)
        return False


def kill_port_processes(port: int, force: bool = False) -> int:
    """Kill all processes on a specific port. Returns count of killed processes."""
    pids = find_processes_on_port(port)
    killed = 0
    
    if not pids:
        return 0
    
    print_colored(f"  Port {port}: Found {len(pids)} process(es)", Colors.CYAN)
    
    for pid in pids:
        if kill_process(pid, force=False):
            killed += 1
            print_colored(f"    ? Killed PID {pid}", Colors.GREEN)
    
    # Wait a moment for graceful shutdown
    if killed > 0:
        time.sleep(1)
    
    # Force kill any remaining processes
    remaining_pids = find_processes_on_port(port)
    if remaining_pids:
        print_colored(f"    Force killing {len(remaining_pids)} remaining process(es)...", Colors.YELLOW)
        for pid in remaining_pids:
            if kill_process(pid, force=True):
                killed += 1
    
    return killed


def kill_all_dev_ports() -> None:
    """Kill all processes on dev server ports."""
    print_colored("?? Killing existing processes on dev ports...", Colors.YELLOW)
    print()
    
    total_killed = 0
    for port in PORTS:
        killed = kill_port_processes(port)
        total_killed += killed
    
    if total_killed > 0:
        print()
        print_colored(f"? Killed {total_killed} process(es) across all ports", Colors.GREEN)
        # Give ports time to fully release
        time.sleep(2)
    else:
        print_colored("? No processes found on dev ports", Colors.GREEN)
    print()


def check_npm_available() -> bool:
    """Check if npm is available."""
    try:
        subprocess.run(["npm", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_node_modules() -> bool:
    """Check if node_modules exists."""
    return Path("node_modules").exists()


def start_all_servers() -> subprocess.Popen:
    """Start all dev servers using npm script."""
    print_colored("?? Starting all dev servers...", Colors.BLUE)
    print()
    
    if not check_npm_available():
        print_colored("? npm is not available. Please install Node.js.", Colors.RED)
        sys.exit(1)
    
    if not check_node_modules():
        print_colored("??  node_modules not found. Installing dependencies...", Colors.YELLOW)
        try:
            subprocess.run(["npm", "install"], check=True)
            print_colored("? Dependencies installed!", Colors.GREEN)
        except subprocess.CalledProcessError:
            print_colored("? Failed to install dependencies.", Colors.RED)
            sys.exit(1)
    
    # Start all servers using the npm script
    try:
        process = subprocess.Popen(
            ["npm", "run", "start:all"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print_colored("? All servers starting...", Colors.GREEN)
        print()
        print_colored("=" * 60, Colors.CYAN)
        print_colored("Servers running on:", Colors.CYAN)
        print_colored("  ? Hub:        http://localhost:1111", Colors.CYAN)
        print_colored("  ? Frontend 1: http://localhost:5555", Colors.CYAN)
        print_colored("  ? Frontend 2: http://localhost:6666", Colors.CYAN)
        print_colored("  ? Frontend 3: http://localhost:7777", Colors.CYAN)
        print_colored("  ? Frontend 4: http://localhost:8888", Colors.CYAN)
        print_colored("  ? Frontend 5: http://localhost:9999", Colors.CYAN)
        print_colored("=" * 60, Colors.CYAN)
        print()
        print_colored("Press Ctrl+C to stop all servers", Colors.YELLOW)
        print()
        
        # Stream output
        if process.stdout:
            for line in iter(process.stdout.readline, ''):
                print(line, end='')
        
        return process
    except FileNotFoundError:
        print_colored("? npm not found. Please install Node.js.", Colors.RED)
        sys.exit(1)
    except Exception as e:
        print_colored(f"? Failed to start servers: {e}", Colors.RED)
        sys.exit(1)


def cleanup(process: subprocess.Popen | None) -> None:
    """Cleanup function for graceful shutdown."""
    print()
    print_colored("\n?? Shutting down servers...", Colors.YELLOW)
    
    if process:
        try:
            # Try graceful shutdown
            if platform.system() == "Windows":
                process.terminate()
            else:
                process.terminate()
            
            # Wait for graceful shutdown
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if needed
                process.kill()
                process.wait()
        except Exception as e:
            print_colored(f"Warning during cleanup: {e}", Colors.YELLOW)
    
    # Kill any remaining processes on ports
    print_colored("Cleaning up ports...", Colors.YELLOW)
    kill_all_dev_ports()
    
    print_colored("? All servers stopped", Colors.GREEN)


def main() -> None:
    """Main execution function."""
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print_colored("=" * 60, Colors.GREEN)
    print_colored("  Pok?mon TCG Dev Servers Manager", Colors.GREEN)
    print_colored("=" * 60, Colors.GREEN)
    print()
    
    # Kill existing processes
    kill_all_dev_ports()
    
    # Set up signal handlers
    process: subprocess.Popen | None = None
    
    def signal_handler(sig, frame):
        cleanup(process)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start all servers
        process = start_all_servers()
        
        # Wait for process to complete
        process.wait()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup(process)


if __name__ == "__main__":
    main()
