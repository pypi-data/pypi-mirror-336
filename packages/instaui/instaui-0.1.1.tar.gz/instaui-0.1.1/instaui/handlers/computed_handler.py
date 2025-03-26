import threading
from typing import Callable, Dict, Optional

from instaui.runtime.context import get_context
from instaui.systems import func_system


ASYNC_URL = "/instaui/computed/async"
SYNC_URL = "/instaui/computed/sync"
INIT_URL = "/instaui/computed/init"

_computed_handlers: Dict[str, Callable] = {}
dict_lock = threading.Lock()


def register_handler(key: str, handler: Callable):
    if key in _computed_handlers:
        return
    with dict_lock:
        _computed_handlers[key] = handler


def get_handler(key: str) -> Optional[Callable]:
    return _computed_handlers.get(key)


def get_statistics_info():
    return {
        "_computed_handlers count": len(_computed_handlers),
        "_computed_handlers keys": list(_computed_handlers.keys()),
    }


def create_handler_key(
    page_path: str,
    handler: Callable,
):
    _, lineno, _ = func_system.get_function_location_info(handler)

    if get_context().debug_mode:
        return f"path:{page_path}|line:{lineno}"
    return f"{page_path}|{lineno}"
