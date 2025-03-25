"""
Setup commands for Build Together CLI

This module handles application initialization, database setup,
and other setup-related commands.
"""

import os
import sys
import click
import subprocess
from pathlib import Path

# Import the echo function for consistent output formatting
from buildtogether.cli import echo

@click.group(name="setup")
def setup_commands():
    """Initialize and configure Build Together."""
    pass

@setup_commands.command()
@click.option("--force", is_flag=True, help="Force setup even if already initialized")
def init(force):
    """Initialize the Build Together application.
    
    This command:
    1. Creates necessary directories
    2. Sets up configuration files
    3. Initializes the database
    """
    echo("Initializing Build Together application...", "info")
    
    # Get or create the application directory
    app_dir = _get_app_directory()
    echo(f"Using application directory: {app_dir}", "info")
    
    # Check if the app is already initialized
    if os.path.exists(os.path.join(app_dir, "instance", "gameplan.db")) and not force:
        echo("Application already initialized. Use --force to reinitialize.", "warning")
        return
    
    # Create instance directory if it doesn't exist
    instance_dir = os.path.join(app_dir, "instance")
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        echo("Created instance directory", "success")
    
    # Initialize the database
    try:
        echo("Initializing database...", "info")
        # Use Python to run the init_db script
        init_db_path = os.path.join(app_dir, "init_db.py")
        subprocess.run([sys.executable, init_db_path], check=True)
        echo("Database initialized successfully", "success")
    except subprocess.CalledProcessError:
        echo("Failed to initialize database", "error")
        sys.exit(1)
    
    # Setup complete
    echo("Build Together application initialized successfully!", "success")
    echo("Run 'btg server start' to start the application server", "info")

@setup_commands.command()
def config():
    """Configure application settings."""
    app_dir = _get_app_directory()
    env_file = os.path.join(app_dir, ".env")
    
    echo("Configuring Build Together application...", "info")
    
    # Check if .env file exists
    if os.path.exists(env_file):
        echo("Configuration file already exists", "info")
        if not click.confirm("Do you want to reconfigure?"):
            return
    
    # Basic configuration
    debug = click.confirm("Enable debug mode?", default=True)
    secret_key = click.prompt("Enter a secret key (or press Enter for a random one)", default="")
    
    # Generate a random secret key if not provided
    if not secret_key:
        import secrets
        secret_key = secrets.token_hex(16)
        echo("Generated random secret key", "info")
    
    # Write configuration to .env file
    with open(env_file, "w") as f:
        f.write(f"FLASK_DEBUG={str(debug).lower()}\n")
        f.write(f"SECRET_KEY={secret_key}\n")
        f.write("BTG_BASE_URL=http://127.0.0.1:5001\n")
    
    echo("Configuration saved to .env file", "success")

# Helper function to get the application directory
def _get_app_directory():
    """Get or create the application directory."""
    # For development, use current directory
    if os.path.exists(os.path.join(os.getcwd(), "app.py")):
        return os.getcwd()
    
    # For installed version, use home directory
    home_dir = Path.home()
    app_dir = os.path.join(home_dir, ".buildtogether")
    
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    
    return app_dir
