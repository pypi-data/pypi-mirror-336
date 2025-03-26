from __future__ import annotations
from typing import Any, Dict, Optional
from .env import env
from instaui.common.jsonable import dumps
from instaui.runtime import get_app_slot
from instaui.runtime.context import get_context

_html_template = env.get_template("web.html")


def render_web_html(
    *,
    config_json: Optional[str] = None,
    config_fetch_url: Optional[str] = None,
    config_fetch_key: Optional[str] = None,
    query_path_params: Optional[str] = None,
    query_params: Optional[Dict] = None,
    query_path: Optional[str] = None,
    page_loadding_json: Optional[str] = None,
    prefix: Any = "",
) -> str:
    if config_json is None and config_fetch_url is None:
        raise ValueError("Either config_json or config_fetch_url must be provided")

    is_remote_config = config_fetch_url is not None
    has_preload = page_loadding_json is not None

    system_slot = get_app_slot()
    resources = system_slot._html_resource

    context = get_context()

    return _html_template.render(
        {
            "is_debug": context.debug_mode,
            "css_links": list(resources._css_links.keys()),
            "style_tags": resources._style_tags,
            "js_links": resources._js_links,
            "script_tags": resources._script_tags,
            "vue_app_use": list(resources._vue_app_use),
            "vue_app_component": list(resources._vue_app_components),
            "import_maps": dumps(resources._import_maps),
            "config_fetch_url": config_fetch_url,
            "config_fetch_key": config_fetch_key,
            "query_path": query_path,
            "query_path_params": query_path_params,
            "query_params": query_params,
            "config_json": config_json,
            "is_remote_config": is_remote_config,
            "has_preload": has_preload,
            "preload_json": page_loadding_json,
            "title": resources.title,
            "prefix": prefix,
        }
    )
