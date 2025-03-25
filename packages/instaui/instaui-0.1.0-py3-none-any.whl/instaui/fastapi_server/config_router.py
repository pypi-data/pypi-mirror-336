from typing import Dict
from fastapi import FastAPI
from contextlib import contextmanager
from instaui.html_tools import to_config_data
from instaui.handlers import config_handler
from instaui.launch_collector import get_launch_collector
from . import _utils


def create_router(app: FastAPI):
    _async_config_handler(app)
    _sync_config_handler(app)


def _async_config_handler(app: FastAPI):
    @app.post(config_handler.ASYNC_URL)
    async def _(data: Dict):
        key = data.get("key", None)
        handler = config_handler.get_handler(key)
        if handler is None:
            return {"error": "event handler not found"}

        _utils.update_app_page_info(data)

        with _execute_request_lifespans():
            await handler()

        return to_config_data()


def _sync_config_handler(app: FastAPI):
    @app.post(config_handler.SYNC_URL)
    def _(data: Dict):
        key = data.get("key", None)

        handler = config_handler.get_handler(key)
        if handler is None:
            return {"error": "event handler not found"}

        _utils.update_app_page_info(data)

        with _execute_request_lifespans():
            handler()

        return to_config_data()


@contextmanager
def _execute_request_lifespans():
    events = [iter(event()) for event in get_launch_collector().page_request_lifespans]
    for event in events:
        next(event)

    yield

    for event in events:
        try:
            next(event)
        except StopIteration:
            pass
