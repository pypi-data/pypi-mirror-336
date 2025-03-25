# Build Together CLI

A lightweight command-line tool for setting up and managing the Build Together application.

## Installation

```bash
pip install buildtogether
```

This will install the `btg` command-line tool.

## Usage

### Initial Setup

Initialize the Build Together application:

```bash
btg setup init
```

Configure application settings:

```bash
btg setup config
```

### Server Management

Start the server:

```bash
btg server start
```

Start with a specific port:

```bash
btg server start --port 8000
```

Handle port conflicts automatically:

```bash
btg server start --auto-port
```

Stop the server:

```bash
btg server stop
```

Restart the server:

```bash
btg server restart
```

Check server status:

```bash
btg server status
```

### Help

Get general help:

```bash
btg --help
```

Get help for a specific command group:

```bash
btg server --help
```

## Development

If you want to develop the CLI tool itself:

1. Clone the repository
2. Navigate to the CLI directory
3. Install in development mode:

```bash
pip install -e .
```

## Features

- Easy application setup and configuration
- Server management (start, stop, restart, status)
- Automatic port conflict detection and resolution
- Colored terminal output for better readability
