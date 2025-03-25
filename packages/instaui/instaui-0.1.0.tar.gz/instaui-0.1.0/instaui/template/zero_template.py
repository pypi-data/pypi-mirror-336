from __future__ import annotations
from typing import Any
from .env import env
from instaui.runtime import get_app_slot


_html_template = env.get_template("zero.html")


def render_zero_html(config_json: str = "{}", prefix: Any = "") -> str:
    resources = get_app_slot()._html_resource

    return _html_template.render(
        {
            "css_links": list(resources._css_links.keys()),
            "style_tags": resources._style_tags,
            "js_links": resources._js_links,
            "script_tags": resources._script_tags,
            "vue_app_use": list(resources._vue_app_use),
            "appConfig": config_json,
            "title": resources.title,
            "prefix": prefix,
        }
    )
