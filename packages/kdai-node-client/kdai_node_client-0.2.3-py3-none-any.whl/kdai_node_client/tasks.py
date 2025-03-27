"""
KDAI Node Client - Task Management

Classes and functions for handling task execution.
"""

import concurrent.futures
import json
import logging
import threading
import time
from typing import Any, Dict, List, Optional, Union

from .exceptions import TaskExecutionError

logger = logging.getLogger("kdai.tasks")


class TaskManager:
    """
    Manager for handling task execution.
    
    This class manages a thread pool for executing tasks received from 
    the KDAI server.
    """
    
    def __init__(self, node, max_workers=None):
        """
        Initialize the task manager.
        
        Args:
            node: The parent KDAINode instance
            max_workers: Maximum number of concurrent worker threads
        """
        self.node = node
        self.max_workers = max_workers
        self.executor = None
        self.running = False
        self.tasks = {}
        self.tasks_lock = threading.Lock()
        
        # Task handlers
        self.task_handlers = {
            "load_model": self._handle_load_model,
            "unload_model": self._handle_unload_model,
            "inference": self._handle_inference,
            "fine_tune": self._handle_fine_tune,
            "train": self._handle_train,
            "distribute": self._handle_distribute,
            "system": self._handle_system,
        }
    
    def start(self):
        """Start the task manager and initialize worker pool."""
        if self.running:
            return
        
        self.running = True
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="kdai-task-"
        )
        logger.info("Task manager started")
    
    def stop(self):
        """Stop the task manager and shut down worker pool."""
        if not self.running:
            return
        
        self.running = False
        if self.executor:
            self.executor.shutdown(wait=False)
            self.executor = None
        logger.info("Task manager stopped")
    
    def add_task(self, task):
        """
        Add a new task to be executed.
        
        Args:
            task: Task data from the server
        """
        if not self.running:
            logger.warning("Task manager not running, ignoring task")
            return
        
        task_id = task.get("_id")
        if not task_id:
            logger.warning("Task without ID, ignoring")
            return
        
        with self.tasks_lock:
            if task_id in self.tasks:
                logger.warning(f"Task {task_id} already exists, ignoring duplicate")
                return
            
            self.tasks[task_id] = {
                "task": task,
                "status": "queued",
                "start_time": None,
                "end_time": None,
                "result": None,
                "future": None,
            }
        
        # Submit task to executor
        future = self.executor.submit(self._execute_task, task_id)
        
        with self.tasks_lock:
            if task_id in self.tasks:
                self.tasks[task_id]["future"] = future
                self.tasks[task_id]["status"] = "submitted"
        
        logger.info(f"Task {task_id} ({task.get('task_type', 'unknown')}) queued for execution")
    
    def _execute_task(self, task_id):
        """
        Execute a task with the given ID.
        
        Args:
            task_id: ID of the task to execute
        
        Returns:
            Task result
        """
        task_data = None
        with self.tasks_lock:
            if task_id not in self.tasks:
                logger.warning(f"Task {task_id} not found for execution")
                return
            
            task_data = self.tasks[task_id]["task"]
            self.tasks[task_id]["status"] = "running"
            self.tasks[task_id]["start_time"] = time.time()
        
        if not task_data:
            return
        
        task_type = task_data.get("task_type")
        logger.info(f"Executing task {task_id} ({task_type})")
        
        # Send task status update
        self._update_task_status(task_id, "processing")
        
        try:
            # Get the appropriate handler for this task type
            handler = self.task_handlers.get(task_type)
            
            if handler:
                result = handler(task_data)
            else:
                logger.warning(f"No handler for task type: {task_type}")
                result = {"error": f"Unsupported task type: {task_type}"}
                self._update_task_status(task_id, "failed", result)
                return result
            
            # Record result and mark task as completed
            with self.tasks_lock:
                if task_id in self.tasks:
                    self.tasks[task_id]["status"] = "completed"
                    self.tasks[task_id]["end_time"] = time.time()
                    self.tasks[task_id]["result"] = result
            
            # Report task completion to server
            self._update_task_status(task_id, "completed", result)
            
            logger.info(f"Task {task_id} completed successfully")
            return result
        
        except Exception as e:
            logger.error(f"Task {task_id} execution failed: {e}", exc_info=True)
            
            # Record error and mark task as failed
            error_result = {"error": str(e)}
            
            with self.tasks_lock:
                if task_id in self.tasks:
                    self.tasks[task_id]["status"] = "failed"
                    self.tasks[task_id]["end_time"] = time.time()
                    self.tasks[task_id]["result"] = error_result
            
            # Report task failure to server
            self._update_task_status(task_id, "failed", error_result)
            
            return error_result
    
    def _update_task_status(self, task_id, status, result=None):
        """
        Send a task status update to the server.
        
        Args:
            task_id: ID of the task
            status: New status string
            result: Task result data (for completed or failed tasks)
        """
        try:
            self.node.report_task_completion(task_id, {
                "status": status,
                "result": result
            })
        except Exception as e:
            logger.error(f"Failed to update task status: {e}")
    
    def get_task_status(self, task_id):
        """
        Get the current status of a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task status information or None if task not found
        """
        with self.tasks_lock:
            return self.tasks.get(task_id)
    
    def list_tasks(self, status=None):
        """
        List all tasks, optionally filtered by status.
        
        Args:
            status: Filter by status (e.g., "running", "completed")
            
        Returns:
            List of task data
        """
        with self.tasks_lock:
            if status:
                return {tid: data for tid, data in self.tasks.items() 
                        if data["status"] == status}
            else:
                return self.tasks.copy()
    
    # Task handlers
    
    def _handle_load_model(self, task):
        """
        Handle a load_model task.
        
        Args:
            task: Task data
            
        Returns:
            Result of model loading
        """
        # Extract task parameters
        params = task.get("parameters", {})
        model_type = params.get("model_type")
        model_id = params.get("model_id")
        
        if not model_type or not model_id:
            raise ValueError("Missing required parameters: model_type, model_id")
        
        logger.info(f"Loading model: {model_id} (type: {model_type})")
        
        # TODO: Implement model loading logic based on model_type
        # This would integrate with Ollama, local models, etc.
        
        # For now, simulate loading
        time.sleep(2)
        
        return {
            "model_id": model_id,
            "model_type": model_type,
            "status": "loaded",
            "memory_used": 1024,  # in MB
        }
    
    def _handle_unload_model(self, task):
        """
        Handle an unload_model task.
        
        Args:
            task: Task data
            
        Returns:
            Result of model unloading
        """
        # Extract task parameters
        params = task.get("parameters", {})
        model_id = params.get("model_id")
        
        if not model_id:
            raise ValueError("Missing required parameter: model_id")
        
        logger.info(f"Unloading model: {model_id}")
        
        # TODO: Implement model unloading logic
        
        # Simulate unloading
        time.sleep(1)
        
        return {
            "model_id": model_id,
            "status": "unloaded",
        }
    
    def _handle_inference(self, task):
        """
        Handle an inference task.
        
        Args:
            task: Task data
            
        Returns:
            Result of model inference
        """
        # Extract task parameters
        params = task.get("parameters", {})
        model_id = params.get("model_id")
        input_text = params.get("input")
        
        if not model_id or not input_text:
            raise ValueError("Missing required parameters: model_id, input")
        
        logger.info(f"Running inference with model: {model_id}")
        
        # TODO: Implement inference logic
        
        # Simulate inference
        time.sleep(3)
        
        return {
            "model_id": model_id,
            "input": input_text,
            "output": f"Simulated response to: {input_text}",
            "execution_time": 3.0,
        }
    
    def _handle_fine_tune(self, task):
        """
        Handle a fine_tune task.
        
        Args:
            task: Task data
            
        Returns:
            Result of fine-tuning
        """
        # Extract task parameters
        params = task.get("parameters", {})
        model_id = params.get("model_id")
        dataset_id = params.get("dataset_id")
        
        if not model_id or not dataset_id:
            raise ValueError("Missing required parameters: model_id, dataset_id")
        
        logger.info(f"Fine-tuning model {model_id} with dataset {dataset_id}")
        
        # TODO: Implement fine-tuning logic
        
        # Simulate fine-tuning with progress updates
        total_steps = 10
        for step in range(1, total_steps + 1):
            progress = (step / total_steps) * 100
            time.sleep(1)
            
            # Send progress update
            self.node.report_task_progress(
                task.get("_id"), 
                progress,
                metrics={
                    "loss": 0.5 - (0.3 * step / total_steps),
                    "accuracy": 0.6 + (0.3 * step / total_steps),
                }
            )
        
        return {
            "model_id": model_id,
            "dataset_id": dataset_id,
            "new_model_id": f"{model_id}_finetuned",
            "training_loss": 0.2,
            "accuracy": 0.9,
        }
    
    def _handle_train(self, task):
        """
        Handle a train task.
        
        Args:
            task: Task data
            
        Returns:
            Result of training
        """
        # Extract task parameters
        params = task.get("parameters", {})
        model_config = params.get("model_config", {})
        dataset_id = params.get("dataset_id")
        
        if not dataset_id:
            raise ValueError("Missing required parameter: dataset_id")
        
        logger.info(f"Training model with dataset {dataset_id}")
        
        # TODO: Implement training logic
        
        # Simulate training with progress updates
        total_epochs = 5
        steps_per_epoch = 10
        
        for epoch in range(1, total_epochs + 1):
            for step in range(1, steps_per_epoch + 1):
                progress = ((epoch - 1) * steps_per_epoch + step) / (total_epochs * steps_per_epoch) * 100
                time.sleep(0.5)
                
                # Send progress update
                self.node.report_task_progress(
                    task.get("_id"),
                    progress,
                    metrics={
                        "epoch": epoch,
                        "step": step,
                        "loss": 1.0 - (0.8 * progress / 100),
                        "accuracy": 0.3 + (0.6 * progress / 100),
                    }
                )
        
        return {
            "model_id": f"new_model_{int(time.time())}",
            "dataset_id": dataset_id,
            "epochs": total_epochs,
            "final_loss": 0.2,
            "final_accuracy": 0.9,
        }
    
    def _handle_distribute(self, task):
        """
        Handle a distributed task (like parameter server).
        
        Args:
            task: Task data
            
        Returns:
            Result of distributed task
        """
        # Extract task parameters
        params = task.get("parameters", {})
        role = params.get("role")
        cluster_id = params.get("cluster_id")
        
        if not role or not cluster_id:
            raise ValueError("Missing required parameters: role, cluster_id")
        
        logger.info(f"Starting distributed task with role: {role} in cluster {cluster_id}")
        
        # TODO: Implement distributed task logic
        
        # Simulate distributed task
        time.sleep(5)
        
        return {
            "role": role,
            "cluster_id": cluster_id,
            "status": "completed",
        }
    
    def _handle_system(self, task):
        """
        Handle system tasks like updates or configuration.
        
        Args:
            task: Task data
            
        Returns:
            Result of system task
        """
        # Extract task parameters
        params = task.get("parameters", {})
        command = params.get("command")
        
        if not command:
            raise ValueError("Missing required parameter: command")
        
        logger.info(f"Executing system command: {command}")
        
        # Handle different system commands
        if command == "update":
            # Simulate update
            time.sleep(2)
            return {
                "command": command,
                "status": "updated",
                "version": "0.1.1",  # Updated version
            }
        elif command == "restart":
            # Schedule node restart
            threading.Timer(2.0, self.node.restart).start()
            return {
                "command": command,
                "status": "restarting",
            }
        else:
            raise ValueError(f"Unknown system command: {command}")
    
    def report_task_progress(self, task_id, progress, metrics=None):
        """
        Report task progress to the server.
        
        Args:
            task_id: ID of the task
            progress: Progress percentage (0-100)
            metrics: Additional metrics to report
        """
        try:
            self.node.report_task_progress(task_id, progress, metrics)
        except Exception as e:
            logger.error(f"Failed to report task progress: {e}")