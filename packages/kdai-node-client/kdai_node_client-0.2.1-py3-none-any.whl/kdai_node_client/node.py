"""
KDAI Node Client - Main Node Class

This module contains the main KDAINode class for connecting to the KDAI platform.
"""

import json
import logging
import os
import platform
import signal
import sys
import threading
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import psutil
import requests
import websocket
from tqdm import tqdm

from .utils import get_gpu_info, get_system_info
from .exceptions import (
    AuthenticationError,
    ConnectionError,
    NodeAlreadyRunningError,
    RequestError,
    TaskExecutionError,
)
from .tasks import TaskManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("kdai")


class KDAINode:
    """
    KDAINode client for connecting to the KDAI distributed AI platform.
    
    This class manages node registration, authentication, system monitoring,
    and task execution through a WebSocket connection to the KDAI server.
    """
    
    def __init__(
        self,
        server_url: str = None,
        auth_token: str = None,
        node_name: str = None,
        config_file: str = None,
    ):
        """
        Initialize a KDAI node client.
        
        Args:
            server_url: URL of the KDAI server
            auth_token: Authentication token for this node
            node_name: Name for this node (used during registration)
            config_file: Path to a configuration file
        """
        self.server_url = server_url
        self.auth_token = auth_token
        self.node_name = node_name or platform.node()
        self.node_id = None
        self.uuid = str(uuid.uuid4())
        self.ws = None
        self.ws_thread = None
        self.running = False
        self.last_heartbeat = None
        self.system_info = None
        self.config_file = config_file or os.path.expanduser("~/.kdai/config.json")
        
        # Task management
        self.task_manager = TaskManager(self)
        
        # Try to load configuration if not provided
        if not self.server_url or not self.auth_token:
            self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file if it exists."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                
                self.server_url = self.server_url or config.get("server_url")
                self.auth_token = self.auth_token or config.get("auth_token")
                self.node_name = self.node_name or config.get("node_name")
                self.node_id = config.get("node_id")
                self.uuid = config.get("uuid", self.uuid)
                
                logger.info(f"Loaded configuration from {self.config_file}")
            except Exception as e:
                logger.warning(f"Failed to load config: {e}")
    
    def _save_config(self) -> None:
        """Save current configuration to file."""
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        
        config = {
            "server_url": self.server_url,
            "auth_token": self.auth_token,
            "node_name": self.node_name,
            "node_id": self.node_id,
            "uuid": self.uuid,
        }
        
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
            logger.info(f"Saved configuration to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def update_system_info(self) -> Dict[str, Any]:
        """Update and return system information about this node."""
        self.system_info = get_system_info()
        return self.system_info
    
    def register(self) -> Dict[str, Any]:
        """
        Register this node with the KDAI server.
        
        Returns:
            Dict containing node registration information including auth_token
        """
        if not self.server_url:
            raise ValueError("Server URL is required for registration")
        
        if not self.node_name:
            raise ValueError("Node name is required for registration")
        
        # Collect system information
        system_info = self.update_system_info()
        
        # Prepare registration data
        reg_data = {
            "name": self.node_name,
            "hostname": platform.node(),
            "uuid": self.uuid,
            "specs": system_info,
        }
        
        # Send registration request
        try:
            reg_url = f"{self.server_url}/api/register_node"
            # Disable redirects to prevent http->https conversion
            response = requests.post(reg_url, json=reg_data, allow_redirects=False)
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                self.auth_token = result.get("auth_token")
                self.node_id = result.get("node_id")
                logger.info(f"Successfully registered node: {self.node_name}")
                self._save_config()
                return result
            else:
                raise AuthenticationError(f"Registration failed: {result.get('message')}")
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to server: {e}")
    
    def authenticate(self) -> bool:
        """
        Authenticate this node with the KDAI server.
        
        Returns:
            Boolean indicating authentication success
        """
        if not self.server_url:
            raise ValueError("Server URL is required for authentication")
        
        if not self.auth_token:
            raise AuthenticationError("Auth token is required for authentication")
        
        try:
            auth_url = f"{self.server_url}/api/node_heartbeat"
            response = requests.post(
                auth_url,
                json={
                    "auth_token": self.auth_token,
                    "node_id": self.node_id,
                    "uuid": self.uuid,
                    "status": "online",
                },
                allow_redirects=False
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                logger.info("Node authentication successful")
                self.last_heartbeat = datetime.now()
                return True
            else:
                raise AuthenticationError(f"Authentication failed: {result.get('message')}")
        except requests.RequestException as e:
            logger.error(f"Failed to connect to server: {e}")
            return False
    
    def heartbeat(self) -> bool:
        """
        Send a heartbeat to the server to maintain connection.
        
        Returns:
            Boolean indicating success
        """
        if not self.auth_token or not self.node_id:
            logger.warning("Cannot send heartbeat without auth token and node ID")
            return False
        
        try:
            system_info = self.update_system_info()
            
            heartbeat_url = f"{self.server_url}/api/node_heartbeat"
            response = requests.post(
                heartbeat_url,
                json={
                    "auth_token": self.auth_token,
                    "node_id": self.node_id,
                    "uuid": self.uuid,
                    "status": "online",
                    "system_info": system_info,
                },
                allow_redirects=False
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.last_heartbeat = datetime.now()
                    # Check for pending tasks
                    tasks = result.get("pending_tasks", [])
                    if tasks:
                        logger.info(f"Received {len(tasks)} pending tasks")
                        for task in tasks:
                            self.task_manager.add_task(task)
                    return True
            
            logger.warning(f"Heartbeat failed: {response.text}")
            return False
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
            return False
    
    def _heartbeat_thread(self) -> None:
        """Background thread that sends periodic heartbeats."""
        while self.running:
            try:
                self.heartbeat()
            except Exception as e:
                logger.error(f"Heartbeat thread error: {e}")
            
            # Sleep for 30 seconds before next heartbeat
            for _ in range(30):
                if not self.running:
                    break
                time.sleep(1)
    
    def report_task_completion(self, task_id: str, result: Dict) -> bool:
        """
        Report task completion to the server.
        
        Args:
            task_id: ID of the completed task
            result: Result data from task execution
            
        Returns:
            Boolean indicating success
        """
        try:
            url = f"{self.server_url}/api/task_complete"
            response = requests.post(
                url,
                json={
                    "auth_token": self.auth_token,
                    "node_id": self.node_id,
                    "task_id": task_id,
                    "result": result,
                },
                allow_redirects=False
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"Task {task_id} completion reported successfully")
                    return True
            
            logger.warning(f"Failed to report task completion: {response.text}")
            return False
        except Exception as e:
            logger.error(f"Error reporting task completion: {e}")
            return False
    
    def connect(self) -> bool:
        """
        Connect to the KDAI server and authenticate.
        
        Returns:
            Boolean indicating connection success
        """
        # First authenticate via REST API
        if not self.authenticate():
            logger.error("Failed to authenticate with server")
            return False
        
        # Then establish WebSocket connection
        ws_url = f"{self.server_url.replace('http', 'ws')}/ws/node/{self.node_id}?token={self.auth_token}"
        
        try:
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open,
            )
            
            # Start WebSocket connection in a separate thread
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            # Wait for connection to establish
            timeout = 10
            start_time = time.time()
            while not hasattr(self.ws, "sock") or not self.ws.sock or not self.ws.sock.connected:
                if time.time() - start_time > timeout:
                    logger.error("WebSocket connection timed out")
                    return False
                time.sleep(0.1)
            
            logger.info("Connected to KDAI server via WebSocket")
            return True
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            return False
    
    def _on_message(self, ws, message):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "task":
                logger.info("Received new task via WebSocket")
                self.task_manager.add_task(data.get("task"))
            elif msg_type == "command":
                logger.info(f"Received command: {data.get('command')}")
                # Handle various commands (shutdown, update, etc.)
                if data.get("command") == "shutdown":
                    self.stop()
            elif msg_type == "ping":
                # Respond to ping
                self.ws.send(json.dumps({"type": "pong"}))
        except Exception as e:
            logger.error(f"Error processing WebSocket message: {e}")
    
    def _on_error(self, ws, error):
        """Handle WebSocket errors."""
        logger.error(f"WebSocket error: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection close."""
        logger.info(f"WebSocket connection closed: {close_msg} (code: {close_status_code})")
        
        # Try to reconnect if we're still running
        if self.running:
            logger.info("Attempting to reconnect in 5 seconds...")
            time.sleep(5)
            self.connect()
    
    def _on_open(self, ws):
        """Handle WebSocket connection open."""
        logger.info("WebSocket connection established")
        # Send initial system info
        self.ws.send(json.dumps({
            "type": "system_info",
            "data": self.update_system_info()
        }))
    
    def start(self, daemon=False) -> None:
        """
        Start the node client and begin processing tasks.
        
        Args:
            daemon: If True, detach and run in background
        """
        if self.running:
            raise NodeAlreadyRunningError("Node is already running")
        
        # Connect to server if not already connected
        if not hasattr(self.ws, "sock") or not self.ws.sock or not self.ws.sock.connected:
            if not self.connect():
                logger.error("Failed to connect to server")
                return
        
        self.running = True
        
        # Start heartbeat thread
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_thread)
        self.heartbeat_thread.daemon = True
        self.heartbeat_thread.start()
        
        # Start task processing
        self.task_manager.start()
        
        logger.info(f"KDAI Node '{self.node_name}' started")
        
        if daemon:
            # Daemonize process (Unix only)
            if os.name != "posix":
                logger.warning("Daemon mode is only supported on Unix systems")
                return
            
            try:
                pid = os.fork()
                if pid > 0:
                    # Exit parent process
                    sys.exit(0)
            except OSError as e:
                logger.error(f"Failed to fork daemon process: {e}")
                sys.exit(1)
            
            # Detach from terminal
            os.setsid()
            os.umask(0)
            
            # Close file descriptors
            sys.stdout.flush()
            sys.stderr.flush()
            with open(os.devnull, "r") as null_in:
                os.dup2(null_in.fileno(), sys.stdin.fileno())
            with open(os.devnull, "w") as null_out:
                os.dup2(null_out.fileno(), sys.stdout.fileno())
                os.dup2(null_out.fileno(), sys.stderr.fileno())
            
            # Write PID file
            pid_file = os.path.expanduser("~/.kdai/kdai-node.pid")
            with open(pid_file, "w") as f:
                f.write(str(os.getpid()))
        else:
            # Run in foreground
            try:
                # Handle keyboard interrupt
                signal.signal(signal.SIGINT, self._signal_handler)
                signal.signal(signal.SIGTERM, self._signal_handler)
                
                # Keep main thread alive
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Interrupted by user")
                self.stop()
    
    def _signal_handler(self, sig, frame):
        """Handle termination signals."""
        logger.info(f"Received signal {sig}, shutting down")
        self.stop()
    
    def stop(self) -> None:
        """Stop the node client and close connections."""
        logger.info("Stopping KDAI Node")
        self.running = False
        
        # Stop task manager
        if hasattr(self, "task_manager"):
            self.task_manager.stop()
        
        # Close WebSocket connection
        if self.ws:
            self.ws.close()
        
        # Update node status to offline
        try:
            requests.post(
                f"{self.server_url}/api/node_heartbeat",
                json={
                    "auth_token": self.auth_token,
                    "node_id": self.node_id,
                    "uuid": self.uuid,
                    "status": "offline",
                },
                allow_redirects=False
            )
        except Exception as e:
            logger.warning(f"Failed to update node status to offline: {e}")
        
        logger.info("KDAI Node stopped")