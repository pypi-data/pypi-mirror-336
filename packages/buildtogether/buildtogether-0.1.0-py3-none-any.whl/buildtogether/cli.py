"""
Main CLI entry point for Build Together

This module defines the primary command-line interface for the 'btg' command.
It sets up the command groups and handles the top-level CLI logic.
"""

import os
import sys
import click
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored terminal output
colorama.init()

# Import command groups
from buildtogether.commands.setup import setup_commands
from buildtogether.commands.server import server_commands

# Create a common output formatting function for consistent styling
def echo(message, level="info"):
    """Print formatted and colored output to the terminal.
    
    Args:
        message (str): The message to display
        level (str): Message level - one of "info", "success", "warning", "error"
    """
    prefix = ""
    if level == "info":
        prefix = f"{Fore.BLUE}[INFO]{Style.RESET_ALL} "
    elif level == "success":
        prefix = f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} "
    elif level == "warning":
        prefix = f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} "
    elif level == "error":
        prefix = f"{Fore.RED}[ERROR]{Style.RESET_ALL} "
    
    click.echo(f"{prefix}{message}")

@click.group()
@click.version_option(package_name="buildtogether")
def main():
    """
    Build Together CLI - Project Management Tool
    
    This tool helps you set up and manage your Build Together application.
    """
    pass

# Add command groups to the main CLI
main.add_command(setup_commands)
main.add_command(server_commands)

# Add any standalone commands here
@main.command()
def info():
    """Display information about Build Together application."""
    echo("Build Together - Project Management Tool", "info")
    echo("Run 'btg setup' to initialize the application", "info")
    echo("Run 'btg server start' to start the server", "info")
    
if __name__ == "__main__":
    main()
