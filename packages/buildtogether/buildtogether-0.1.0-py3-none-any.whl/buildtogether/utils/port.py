"""
Port utility functions for Build Together CLI

This module provides functions to check port availability and find open ports.
"""

import socket
import psutil

def is_port_in_use(port):
    """
    Check if a port is already in use on the system.
    
    Args:
        port (int): The port number to check
        
    Returns:
        bool: True if the port is in use, False otherwise
    """
    # Method 1: Try to create a socket and bind to the port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Set the socket to reuse the address if in TIME_WAIT state
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Try to bind to the port
            s.bind(('127.0.0.1', port))
            return False
        except socket.error:
            # If binding fails, the port is in use
            pass
    
    # Method 2: Check system connections
    # This can detect ports used by other processes
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port and conn.status == 'LISTEN':
            return True
    
    # If we get here through Method 1 check but not Method 2,
    # the port might be in a transitional state, so return True to be safe
    return True

def find_available_port(start_port=5000, max_port=5999):
    """
    Find an available port starting from start_port up to max_port.
    
    Args:
        start_port (int): The starting port to check from
        max_port (int): The maximum port number to check
        
    Returns:
        int: An available port number, or None if no ports are available
    """
    for port in range(start_port, max_port + 1):
        if not is_port_in_use(port):
            return port
    return None
