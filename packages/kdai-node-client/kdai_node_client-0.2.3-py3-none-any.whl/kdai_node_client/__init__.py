"""
KDAI Node Client

A Python client library for connecting computing nodes to the KDAI distributed AI platform.
"""

from .node import KDAINode
from .version import __version__

__all__ = ["KDAINode", "__version__"]