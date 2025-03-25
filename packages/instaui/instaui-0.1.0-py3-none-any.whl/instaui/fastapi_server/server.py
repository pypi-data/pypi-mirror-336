from __future__ import annotations
import inspect
import os
import multiprocessing
from pathlib import Path
from typing import Any, Optional, Set
import __main__

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from uvicorn.supervisors import ChangeReload

from instaui.html_tools import to_json
from instaui.launch_collector import get_launch_collector
from instaui.page_info import PageInfo
from instaui.handlers import config_handler
from instaui.systems import file_system
from instaui import consts
from instaui.runtime._app import get_app_slot
from instaui.template import web_template
from . import config_router
from . import event_router
from . import watch_router
from . import debug_mode_router
from .middlewares import RequestContextMiddleware
from ._uvicorn import UvicornServer


APP_IMPORT_STRING = "instaui.fastapi_server.server:Server._instance.app"


class Server:
    _instance: Optional[Server] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.app = FastAPI()
        self.app.add_middleware(RequestContextMiddleware)
        config_router.create_router(self.app)
        event_router.create_router(self.app)
        watch_router.create_router(self.app)
        debug_mode_router.create_router(self.app)

        self._static_dir_url = _add_static_dir(self.app)

        for page_info in get_launch_collector()._page_router.values():
            self.register_page(page_info)

        self._registered_static_routes: Set[str] = set()

    def register_page(self, info: PageInfo):
        is_async = inspect.iscoroutinefunction(info.func)

        self._remove_route(info.path)

        key = info.create_key()
        config_handler.register_handler(key, info.func)
        config_fetch_url = (
            config_handler.ASYNC_URL if is_async else config_handler.SYNC_URL
        )

        @self.app.get(info.path)
        def wrapper(request: Request):
            page_loadding_json = None
            if info.page_loading:
                loadding_result = info.page_loading()
                if loadding_result:
                    return loadding_result
                page_loadding_json = to_json()

            html = self._to_web_html(
                page_info=info,
                config_fetch_url=config_fetch_url,
                config_fetch_key=key,
                query_path=info.path,
                request=request,
                page_loadding_json=page_loadding_json,
            )
            response = HTMLResponse(html)
            return response

        return wrapper

    def _to_web_html(
        self,
        *,
        page_info: PageInfo,
        query_path: str,
        config_json: Optional[str] = None,
        config_fetch_url: Optional[str] = None,
        config_fetch_key: Optional[str] = None,
        page_loadding_json: Optional[str] = None,
        request: Request,
    ):
        system_slot = get_app_slot()
        html_resource = system_slot._html_resource
        page_info.apply_settings(html_resource)

        html_resource.add_import_map(
            "vue", self._static_dir_url + f"/{consts.VUE_ES_JS_PATH.name}"
        )

        html_resource.add_import_map(
            "instaui", self._static_dir_url + f"/{consts.APP_ES_JS_PATH.name}"
        )
        html_resource.add_css_link(consts.APP_CSS_PATH)

        if html_resource.use_tailwind:
            tailwind_url = self._static_dir_url + f"/{consts.TAILWIND_JS_PATH.name}"
            html_resource.add_js_link(tailwind_url)

        # register custom components
        # TODO: use one get api to get all components
        for component in system_slot._js_components:
            if not component.esm:
                continue
            url = self.add_static_file_route(component.esm)
            html_resource.add_vue_app_component(name=component.name, url=url)

            if component.css:
                for css_link in component.css:
                    html_resource.add_css_link(css_link)

        # register custom plugins
        for plugin in system_slot._plugins:
            if not plugin.esm:
                continue
            url = self.add_static_file_route(plugin.esm)
            html_resource.add_vue_app_use(url)

            if plugin.css:
                for css_link in plugin.css:
                    html_resource.add_css_link(css_link)

        # css file link to web static link
        html_resource._css_links = {
            self.add_static_file_route(link) if isinstance(link, Path) else link: None
            for link, attrs in html_resource._css_links.items()
        }

        # js file link to web static link
        for info in html_resource._js_links:
            if isinstance(info.link, Path):
                info.link = self.add_static_file_route(info.link)

        prefix = request.headers.get(
            "X-Forwarded-Prefix", request.scope.get("root_path", "")
        )

        result = web_template.render_web_html(
            config_json=config_json,
            config_fetch_url=config_fetch_url,
            config_fetch_key=config_fetch_key,
            query_path_params=str(request.path_params),
            query_params=dict(request.query_params),
            query_path=query_path,
            page_loadding_json=page_loadding_json,
            prefix=prefix,
        )
        get_app_slot().reset_html_resource()
        return result

    def add_static_file_route(self, local_file: Path) -> str:
        path = file_system.generate_static_url_from_file_path(local_file)
        if path in self._registered_static_routes:
            return path

        @self.app.get(path)
        def _() -> FileResponse:
            return FileResponse(
                local_file, headers={"Cache-Control": "public, max-age=3600"}
            )

        return path

    def _remove_route(self, path: str) -> None:
        self.app.routes[:] = [
            r for r in self.app.routes if getattr(r, "path", None) != path
        ]

    def try_close_server(self):
        UvicornServer.instance.should_exit = True

    def run(
        self,
        host="0.0.0.0",
        port=8080,
        reload: bool = True,
        reload_dirs: str = ".",
        reload_includes: str = "*.py",
        reload_excludes: str = ".*, .py[cod], .sw.*, ~*",
        log_level="info",
        workers: int | None = None,
        uds: str | None = None,
        **kwargs: Any,
    ):
        if multiprocessing.current_process().name != "MainProcess":
            return

        if reload and not hasattr(__main__, "__file__"):
            reload = False

        config = uvicorn.Config(
            APP_IMPORT_STRING if reload else self.app,
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
            workers=workers,
            uds=uds,
            reload_includes=_split_args(reload_includes) if reload else None,
            reload_excludes=_split_args(reload_excludes) if reload else None,
            reload_dirs=_split_args(reload_dirs) if reload else None,
            **kwargs,
        )

        UvicornServer.create_singleton(config, [debug_mode_router.when_server_reload])

        if config.should_reload:
            ChangeReload(config, target=UvicornServer.instance.run, sockets=[]).run()
        else:
            UvicornServer.instance.run()

        if config.uds:
            os.remove(config.uds)  # pragma: py-win32

    def run_with(self, app):
        assert isinstance(app, FastAPI), "app must be a FastAPI instance"


def _add_static_dir(app: FastAPI):
    url = file_system.generate_static_url_from_file_path(consts._STATIC_DIR)
    app.mount(url, StaticFiles(directory=consts._STATIC_DIR))
    return url


def _split_args(args: str):
    return [a.strip() for a in args.split(",")]
