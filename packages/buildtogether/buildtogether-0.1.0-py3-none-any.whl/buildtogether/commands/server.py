"""
Server management commands for Build Together CLI

This module handles starting, stopping, and managing the application server.
It includes port conflict detection and resolution functionality.
"""

import os
import sys
import time
import signal
import psutil
import subprocess
import socket
from pathlib import Path

import click

# Import the echo function for consistent output formatting
from buildtogether.cli import echo
from buildtogether.utils.port import find_available_port, is_port_in_use

# Default port for the Build Together application
DEFAULT_PORT = 5001

@click.group(name="server")
def server_commands():
    """Manage the Build Together server."""
    pass

@server_commands.command()
@click.option("--port", type=int, default=DEFAULT_PORT, help="Port to run the server on")
@click.option("--auto-port", is_flag=True, help="Automatically find an open port if the default is in use")
def start(port, auto_port):
    """Start the Build Together server.
    
    This command starts the Flask development server.
    If the requested port is in use and --auto-port is specified,
    it will try to find an available port.
    """
    app_dir = _get_app_directory()
    pid_file = _get_pid_file_path(app_dir)
    
    # Check if server is already running
    if _is_server_running(pid_file):
        existing_pid = _get_server_pid(pid_file)
        existing_port = _get_server_port(existing_pid)
        echo(f"Server is already running (PID: {existing_pid}, Port: {existing_port})", "warning")
        echo(f"Use 'btg server stop' to stop the server first", "info")
        return
    
    # Check if the port is in use
    if is_port_in_use(port):
        if auto_port:
            old_port = port
            port = find_available_port(start_port=port)
            echo(f"Port {old_port} is in use. Using port {port} instead.", "warning")
        else:
            echo(f"Port {port} is already in use. Use --auto-port to find an available port.", "error")
            echo(f"Or use 'btg server stop' to stop any running servers.", "info")
            return
    
    # Start the server
    echo(f"Starting Build Together server on port {port}...", "info")
    
    # Set environment variables
    env = os.environ.copy()
    env["FLASK_APP"] = "app.py"
    env["FLASK_DEBUG"] = "1"  # Enable debug mode for development
    env["PORT"] = str(port)
    
    # Use Python to run the app.py script
    try:
        # Start the server as a subprocess
        cmd = [sys.executable, os.path.join(app_dir, "app.py")]
        process = subprocess.Popen(
            cmd,
            cwd=app_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # Use a new process group so we can properly terminate it later
            start_new_session=True
        )
        
        # Save the PID to a file for later management
        with open(pid_file, "w") as f:
            f.write(f"{process.pid}\\n{port}")
        
        # Wait a moment to see if it starts successfully
        time.sleep(1)
        if process.poll() is not None:
            # Process terminated immediately
            stdout, stderr = process.communicate()
            echo("Server failed to start", "error")
            echo(f"Error: {stderr.decode('utf-8')}", "error")
            os.unlink(pid_file)
            return
        
        echo(f"Server started successfully on port {port}", "success")
        echo(f"You can access the application at http://127.0.0.1:{port}", "info")
        echo(f"Press Ctrl+C to stop the server or run 'btg server stop'", "info")
        
        # If not running in a terminal, just return
        if not sys.stdout.isatty():
            return
            
        # Wait for Ctrl+C or other termination
        try:
            while True:
                if process.poll() is not None:
                    # Process terminated
                    break
                time.sleep(0.5)
        except KeyboardInterrupt:
            _stop_server(process.pid)
            echo("Server stopped", "info")
            if os.path.exists(pid_file):
                os.unlink(pid_file)
                
    except Exception as e:
        echo(f"Error starting server: {str(e)}", "error")
        if os.path.exists(pid_file):
            os.unlink(pid_file)

@server_commands.command()
def stop():
    """Stop the Build Together server."""
    app_dir = _get_app_directory()
    pid_file = _get_pid_file_path(app_dir)
    
    if not _is_server_running(pid_file):
        echo("No server is currently running", "warning")
        # Clean up any stale PID file
        if os.path.exists(pid_file):
            os.unlink(pid_file)
        return
    
    pid = _get_server_pid(pid_file)
    if pid:
        echo(f"Stopping server (PID: {pid})...", "info")
        if _stop_server(pid):
            echo("Server stopped successfully", "success")
        else:
            echo("Failed to stop server gracefully, forcing termination", "warning")
            _stop_server(pid, force=True)
    
    # Remove the PID file
    if os.path.exists(pid_file):
        os.unlink(pid_file)

@server_commands.command()
@click.option("--port", type=int, default=None, help="Port to run the server on")
@click.option("--auto-port", is_flag=True, help="Automatically find an open port if the default is in use")
def restart(port, auto_port):
    """Restart the Build Together server."""
    app_dir = _get_app_directory()
    pid_file = _get_pid_file_path(app_dir)
    
    # Get current port if server is running
    current_port = None
    if _is_server_running(pid_file):
        pid = _get_server_pid(pid_file)
        current_port = _get_server_port(pid)
        
    # Use current port if none specified
    if port is None and current_port is not None:
        port = current_port
    elif port is None:
        port = DEFAULT_PORT
    
    # Stop the server if it's running
    if _is_server_running(pid_file):
        echo("Stopping server for restart...", "info")
        stop.callback()
        # Brief pause to ensure proper shutdown
        time.sleep(1)
    
    # Start the server with the specified port
    start.callback(port=port, auto_port=auto_port)

@server_commands.command()
def status():
    """Check the status of the Build Together server."""
    app_dir = _get_app_directory()
    pid_file = _get_pid_file_path(app_dir)
    
    if _is_server_running(pid_file):
        pid = _get_server_pid(pid_file)
        port = _get_server_port(pid)
        echo(f"Server is running", "success")
        echo(f"PID: {pid}", "info")
        echo(f"Port: {port}", "info")
        echo(f"URL: http://127.0.0.1:{port}", "info")
    else:
        echo("Server is not running", "warning")
        # Clean up any stale PID file
        if os.path.exists(pid_file):
            os.unlink(pid_file)

# Helper functions
def _get_app_directory():
    """Get the application directory."""
    # For development, use current directory
    if os.path.exists(os.path.join(os.getcwd(), "app.py")):
        return os.getcwd()
    
    # For installed version, use home directory
    home_dir = Path.home()
    app_dir = os.path.join(home_dir, ".buildtogether")
    
    return app_dir

def _get_pid_file_path(app_dir):
    """Get the path to the PID file."""
    return os.path.join(app_dir, ".btg.pid")

def _is_server_running(pid_file):
    """Check if the server is running."""
    if not os.path.exists(pid_file):
        return False
    
    pid = _get_server_pid(pid_file)
    if pid is None:
        return False
    
    # Check if the process is running
    try:
        process = psutil.Process(pid)
        # Verify it's our server process (could check command line for "app.py")
        return process.is_running()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

def _get_server_pid(pid_file):
    """Get the server PID from the PID file."""
    try:
        with open(pid_file, "r") as f:
            content = f.read().strip().split("\\n")
            return int(content[0])
    except (IOError, ValueError, IndexError):
        return None

def _get_server_port(pid):
    """Get the port the server is running on."""
    # First try to get from PID file
    app_dir = _get_app_directory()
    pid_file = _get_pid_file_path(app_dir)
    
    try:
        with open(pid_file, "r") as f:
            content = f.read().strip().split("\\n")
            if len(content) > 1:
                return int(content[1])
    except (IOError, ValueError, IndexError):
        pass
    
    # Fallback: Try to determine from process connections
    try:
        process = psutil.Process(pid)
        connections = process.connections(kind='inet')
        for conn in connections:
            if conn.status == 'LISTEN':
                return conn.laddr.port
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    
    return DEFAULT_PORT

def _stop_server(pid, force=False):
    """Stop the server process."""
    try:
        process = psutil.Process(pid)
        if force:
            # Force kill the process
            process.kill()
        else:
            # Try graceful termination first
            process.terminate()
            # Wait for process to terminate
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                # If it doesn't terminate in 5 seconds, force kill
                process.kill()
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False
