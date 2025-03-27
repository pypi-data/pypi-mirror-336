"""
KDAI Node Client - Command Line Interface

Command-line interface for the KDAI Node Client.
"""

import argparse
import json
import logging
import os
import sys
import time

from .node import KDAINode
from .version import __version__

logger = logging.getLogger("kdai.cli")


def setup_logging(verbose=False):
    """Configure logging based on verbosity level."""
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),
        ]
    )
    
    # Also log to file in ~/.kdai/logs
    try:
        log_dir = os.path.expanduser("~/.kdai/logs")
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "kdai-node.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Failed to set up file logging: {e}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="KDAI Node Client")
    parser.add_argument("--version", action="version", version=f"KDAI Node Client v{__version__}")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Register command
    register_parser = subparsers.add_parser("register", help="Register a new node")
    register_parser.add_argument("--server-url", required=True, help="URL of the KDAI server")
    register_parser.add_argument("--name", required=True, help="Name for this node")
    
    # Connect command
    connect_parser = subparsers.add_parser("connect", help="Connect an existing node")
    connect_parser.add_argument("--server-url", help="URL of the KDAI server")
    connect_parser.add_argument("--token", help="Authentication token for this node")
    connect_parser.add_argument("--config", help="Path to configuration file")
    
    # Start command
    start_parser = subparsers.add_parser("start", help="Start the node client")
    start_parser.add_argument("--daemon", action="store_true", help="Run as a daemon in the background")
    start_parser.add_argument("--server-url", help="URL of the KDAI server")
    start_parser.add_argument("--token", help="Authentication token for this node")
    start_parser.add_argument("--config", help="Path to configuration file")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check node status")
    
    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop a running node")
    
    return parser.parse_args()


def register_node(args):
    """Register a new node with the KDAI server."""
    node = KDAINode(server_url=args.server_url, node_name=args.name)
    
    try:
        result = node.register()
        print(f"Node registered successfully!")
        print(f"Node ID: {node.node_id}")
        print(f"Auth Token: {node.auth_token}")
        print("\nIMPORTANT: Save this auth token, it's required to reconnect the node.")
        print(f"Configuration saved to: {node.config_file}")
        
        return 0
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        return 1


def connect_node(args):
    """Connect an existing node to the KDAI server."""
    config_file = args.config if args.config else None
    
    node = KDAINode(
        server_url=args.server_url,
        auth_token=args.token,
        config_file=config_file
    )
    
    try:
        if node.connect():
            print(f"Connected to KDAI server at {node.server_url}")
            print(f"Node ID: {node.node_id}")
            print(f"Node status: Online")
            return 0
        else:
            print("Failed to connect to KDAI server")
            return 1
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return 1


def start_node(args):
    """Start the node client."""
    config_file = args.config if args.config else None
    
    node = KDAINode(
        server_url=args.server_url,
        auth_token=args.token,
        config_file=config_file
    )
    
    try:
        if not node.server_url or not node.auth_token:
            logger.error("Missing server URL or auth token. Use --server-url and --token options or register the node first.")
            return 1
        
        print(f"Starting KDAI Node '{node.node_name}'")
        print(f"Server URL: {node.server_url}")
        
        if args.daemon:
            print("Running in daemon mode")
            node.start(daemon=True)
            return 0
        else:
            print("Press Ctrl+C to stop")
            node.start(daemon=False)
            return 0
    except KeyboardInterrupt:
        print("Interrupted by user")
        node.stop()
        return 0
    except Exception as e:
        logger.error(f"Failed to start node: {e}")
        return 1


def check_status():
    """Check the status of a running node."""
    pid_file = os.path.expanduser("~/.kdai/kdai-node.pid")
    
    if not os.path.exists(pid_file):
        print("No running node found")
        return 1
    
    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
        
        import psutil
        if psutil.pid_exists(pid):
            proc = psutil.Process(pid)
            
            # Check if this is actually our process
            if "kdai-node" in " ".join(proc.cmdline()):
                print(f"KDAI Node is running (PID: {pid})")
                print(f"Started at: {time.ctime(proc.create_time())}")
                print(f"Memory usage: {proc.memory_info().rss / (1024 * 1024):.2f} MB")
                print(f"CPU usage: {proc.cpu_percent(interval=0.1):.1f}%")
                
                # Try to load config for more info
                config_file = os.path.expanduser("~/.kdai/config.json")
                if os.path.exists(config_file):
                    with open(config_file, "r") as f:
                        config = json.load(f)
                    print(f"Node name: {config.get('node_name', 'Unknown')}")
                    print(f"Server URL: {config.get('server_url', 'Unknown')}")
                
                return 0
            else:
                print(f"PID {pid} exists but is not a KDAI Node process")
                return 1
        else:
            print(f"No running node found (stale PID file)")
            return 1
    except Exception as e:
        logger.error(f"Failed to check status: {e}")
        return 1


def stop_node():
    """Stop a running node."""
    pid_file = os.path.expanduser("~/.kdai/kdai-node.pid")
    
    if not os.path.exists(pid_file):
        print("No running node found")
        return 1
    
    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
        
        import psutil
        if psutil.pid_exists(pid):
            proc = psutil.Process(pid)
            
            # Check if this is actually our process
            if "kdai-node" in " ".join(proc.cmdline()):
                print(f"Stopping KDAI Node (PID: {pid})")
                proc.terminate()
                
                # Wait for process to terminate
                try:
                    proc.wait(timeout=10)
                    print("Node stopped successfully")
                except psutil.TimeoutExpired:
                    print("Node did not terminate, forcing stop...")
                    proc.kill()
                
                # Remove PID file
                os.unlink(pid_file)
                return 0
            else:
                print(f"PID {pid} exists but is not a KDAI Node process")
                return 1
        else:
            print(f"No running node found (stale PID file)")
            os.unlink(pid_file)
            return 1
    except Exception as e:
        logger.error(f"Failed to stop node: {e}")
        return 1


def main():
    """Main entry point for the CLI."""
    args = parse_args()
    setup_logging(verbose=args.verbose)
    
    if args.command == "register":
        return register_node(args)
    elif args.command == "connect":
        return connect_node(args)
    elif args.command == "start":
        return start_node(args)
    elif args.command == "status":
        return check_status()
    elif args.command == "stop":
        return stop_node()
    else:
        print("No command specified. Use --help for usage information.")
        return 1


if __name__ == "__main__":
    sys.exit(main())