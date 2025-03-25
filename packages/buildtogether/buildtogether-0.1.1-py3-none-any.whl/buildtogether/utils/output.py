"""
Output utilities for the buildtogether CLI.
"""
import click
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def echo(message, level="info", nl=True):
    """
    Display a colored message based on level.
    
    Args:
        message (str): The message to display
        level (str): The message level (info, success, warning, error)
        nl (bool): Whether to add a newline
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
    
    click.echo(f"{prefix}{message}", nl=nl)
