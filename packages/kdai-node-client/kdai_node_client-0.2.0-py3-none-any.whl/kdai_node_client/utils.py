"""
KDAI Node Client - Utility Functions

Utility functions for system information gathering and other helper tasks.
"""

import json
import logging
import math
import os
import platform
import socket
import subprocess
import uuid
from typing import Dict, List, Optional, Union

import psutil

logger = logging.getLogger("kdai.utils")


def get_system_info() -> Dict[str, Union[str, int, float, Dict]]:
    """
    Collect detailed system information about this node.
    
    Returns:
        Dictionary containing system specifications
    """
    system_info = {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "cpu_percent": psutil.cpu_percent(),
        "ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "ram_available_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        "disk_total_gb": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
        "disk_free_gb": round(psutil.disk_usage('/').free / (1024 ** 3), 2),
    }
    
    # Add GPU information if available
    gpu_info = get_gpu_info()
    if gpu_info:
        system_info["gpus"] = gpu_info
        system_info["gpu_count"] = len(gpu_info)
    else:
        system_info["gpus"] = []
        system_info["gpu_count"] = 0
    
    return system_info


def get_gpu_info() -> List[Dict[str, Union[str, int, float]]]:
    """
    Attempt to gather information about available GPUs.
    
    Returns:
        List of dictionaries with GPU information or empty list if none found
    """
    gpus = []
    
    # Try to get NVIDIA GPU info using nvidia-smi
    try:
        nvidia_smi_output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free,memory.used,temperature.gpu,utilization.gpu", 
             "--format=csv,noheader,nounits"],
            universal_newlines=True
        )
        
        for i, line in enumerate(nvidia_smi_output.strip().split("\n")):
            values = [val.strip() for val in line.split(",")]
            if len(values) >= 6:
                gpu = {
                    "index": i,
                    "name": values[0],
                    "type": "NVIDIA",
                    "memory_total_mb": float(values[1]),
                    "memory_free_mb": float(values[2]),
                    "memory_used_mb": float(values[3]),
                    "temperature": float(values[4]),
                    "utilization": float(values[5]),
                }
                gpus.append(gpu)
        
        return gpus
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.debug("nvidia-smi not found or failed")
    
    # Try to get AMD GPU info using rocm-smi
    try:
        rocm_smi_output = subprocess.check_output(
            ["rocm-smi", "--showuse", "--showmeminfo", "vram", "--json"],
            universal_newlines=True
        )
        data = json.loads(rocm_smi_output)
        
        for i, (gpu_id, gpu_data) in enumerate(data.items()):
            if isinstance(gpu_data, dict):
                memory_info = gpu_data.get("memory usage", {}).get("vram", {})
                gpu = {
                    "index": i,
                    "name": gpu_data.get("card_name", f"AMD GPU {i}"),
                    "type": "AMD",
                    "memory_total_mb": float(memory_info.get("total", 0)),
                    "memory_used_mb": float(memory_info.get("used", 0)),
                    "memory_free_mb": float(memory_info.get("free", 0)),
                    "utilization": float(gpu_data.get("gpu use (%)", 0)),
                }
                gpus.append(gpu)
        
        return gpus
    except (subprocess.SubprocessError, FileNotFoundError, json.JSONDecodeError):
        logger.debug("rocm-smi not found or failed")
    
    # Check for Apple Silicon (M1/M2) GPU
    if platform.system() == "Darwin" and platform.processor() == "arm":
        try:
            # Use sysctl to get information about the SOC
            sysctl_output = subprocess.check_output(
                ["sysctl", "-n", "hw.memsize", "hw.ncpu", "machdep.cpu.brand_string"],
                universal_newlines=True
            ).strip().split("\n")
            
            if len(sysctl_output) >= 3:
                total_memory = int(sysctl_output[0]) / (1024 ** 3)  # Convert to GB
                gpu = {
                    "index": 0,
                    "name": f"Apple Silicon ({sysctl_output[2]})",
                    "type": "Apple",
                    "memory_total_mb": total_memory * 1024,  # Total system memory in MB
                    "memory_free_mb": None,  # Can't determine GPU-specific memory
                    "memory_used_mb": None,
                    "utilization": None,
                }
                gpus.append(gpu)
        except (subprocess.SubprocessError, ValueError, IndexError):
            logger.debug("Failed to get Apple Silicon GPU info")
    
    return gpus


def get_network_interfaces() -> Dict[str, Dict]:
    """
    Get information about network interfaces.
    
    Returns:
        Dictionary of network interfaces with details
    """
    interfaces = {}
    
    for name, addrs in psutil.net_if_addrs().items():
        interface = {"addresses": []}
        
        for addr in addrs:
            address_info = {
                "family": str(addr.family),
                "address": addr.address,
                "netmask": addr.netmask,
                "broadcast": addr.broadcast,
            }
            interface["addresses"].append(address_info)
        
        # Get stats
        if name in psutil.net_if_stats():
            stats = psutil.net_if_stats()[name]
            interface["speed"] = stats.speed
            interface["mtu"] = stats.mtu
            interface["up"] = stats.isup
            interface["duplex"] = stats.duplex
        
        interfaces[name] = interface
    
    return interfaces


def get_local_ip() -> str:
    """
    Get the local IP address of this machine.
    
    Returns:
        Local IP address as string
    """
    try:
        # Create a socket connection to an external server
        # This is the most reliable way to get the correct local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        # Fallback method
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)


def human_readable_size(size_bytes: int) -> str:
    """
    Convert bytes to a human-readable size string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string (e.g., "1.23 GB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"