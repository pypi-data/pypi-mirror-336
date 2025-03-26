from typing import Callable, Dict

ASYNC_URL = "/instaui/config/async"
SYNC_URL = "/instaui/config/sync"
_handlers: Dict[str, Callable] = {}


def register_handler(key: str, handler: Callable):
    _handlers[key] = handler


def get_handler(key: str) -> Callable:
    return _handlers[key]
