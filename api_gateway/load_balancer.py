"""
Very small round-robin load balancer.

`get_next_service("user")` returns the next backend URL for that group.
"""
import itertools
from typing import Dict, List

from .config import get_settings

settings = get_settings()

# Parse comma-separated env vars into list[str]
_backends: Dict[str, List[str]] = {
    "user": [f"http://{h}" for h in settings.USER_BACKENDS.split(",")],
    "transaction": [f"http://{h}" for h in settings.TX_BACKENDS.split(",")],
}
_cycle = {k: itertools.cycle(v) for k, v in _backends.items()}


def get_next_service(group: str) -> str:
    """Return next backend URL for the given group (round-robin)."""
    return next(_cycle[group])
