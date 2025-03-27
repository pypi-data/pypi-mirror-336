# KDAI Node Client

The official client library for connecting nodes to the KDAI distributed AI platform.

## Features

- Simple node registration and authentication
- Secure WebSocket-based communication with KDAI hub
- Task management for AI workloads
- Resource utilization monitoring
- Simple CLI interface

## Installation

```bash
pip install kdai-node-client
```

## Quick Start

### Register a New Node

To register a new node with your KDAI server:

```bash
# Register a new node
kdai-node register --server-url https://your-kdai-server.com --name "My AI Node"
```

This will generate an authentication token for your node and save the configuration.

### Start the Node

Once registered, you can start the node:

```bash
# Start the node
kdai-node start
```

The node will connect to the KDAI server, report its system information, and start accepting tasks.

## Advanced Usage

### Monitor Node Status

Check the status of your node:

```bash
kdai-node status
```

### Stop Node

Stop a running node:

```bash
kdai-node stop
```

### Programmatic Usage

You can also use the KDAI Node Client as a library in your Python code:

```python
from kdai_node_client import KDAINode

# Create a node instance
node = KDAINode(server_url="https://your-kdai-server.com", node_name="My AI Node")

# Register the node
node.register()

# Start the node
node.start()

# To stop the node
node.stop()
```

## API Reference

Full API documentation is available at https://docs.kdai.io/node-client/

## Requirements

- Python 3.8 or higher
- Working network connection to KDAI server
- WebSocket support

## License

MIT License