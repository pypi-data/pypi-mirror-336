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
from buildtogether.utils.output import echo

# Initialize colorama for cross-platform colored terminal output
colorama.init()

# Import command groups
from buildtogether.commands.setup import setup_commands
from buildtogether.commands.server import server_commands

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
