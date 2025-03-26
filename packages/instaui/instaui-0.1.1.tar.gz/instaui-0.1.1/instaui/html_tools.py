from __future__ import annotations
from pathlib import Path
from typing import Dict, Literal, Optional, Union
import instaui.consts as consts
from instaui.common.jsonable import dumps, dumps2dict
from instaui.runtime import get_app_slot, HtmlResource
from instaui.template import render_zero_html


def add_css_link(href: Union[str, Path], *, shared: bool = False):
    if shared:
        HtmlResource.default_css_link(href)

    get_app_slot()._html_resource.add_css_link(href)


def add_js_link(
    link: Union[str, Path],
    *,
    shared: bool = False,
    type: Optional[Literal["module", "importmap"]] = None,
):
    attrs = {
        "type": type,
    }

    if shared:
        HtmlResource.default_js_link(link, attrs=attrs)

    get_app_slot()._html_resource.add_js_link(link, attrs=attrs)


def add_style(content: str, *, shared: bool = False):
    if shared:
        HtmlResource.default_style_tag(content)
    get_app_slot()._html_resource.add_style_tag(content)


def add_js_code(code: str, *, shared: bool = False):
    if shared:
        HtmlResource.default_script_tag(code)
    get_app_slot()._html_resource.add_script_tag(code)


def add_vue_app_use(name: str, *, shared: bool = False):
    if shared:
        HtmlResource.default_vue_app_use(name)
    get_app_slot()._html_resource.add_vue_app_use(name)


def to_config_data() -> Dict:
    return dumps2dict(get_app_slot())


def to_json(indent=False):
    return dumps(get_app_slot(), indent=indent)


def to_html(file: Union[str, Path]):
    if isinstance(file, str):
        import inspect

        frame = inspect.currentframe().f_back  # type: ignore
        assert frame is not None
        script_file = inspect.getfile(frame)
        file = Path(script_file).parent.joinpath(file)

    file = Path(file)
    system_slot = get_app_slot()
    html_resource = system_slot._html_resource

    if html_resource.use_tailwind:
        html_resource.add_js_link(consts.TAILWIND_JS_PATH, insert_before=0)
    html_resource.add_js_link(consts.APP_IIFE_JS_PATH, insert_before=0)
    html_resource.add_js_link(consts.VUE_IIFE_JS_PATH, insert_before=0)
    html_resource.add_css_link(consts.APP_CSS_PATH)

    # register custom components
    for component in system_slot._js_components:
        if not component.iife:
            continue

        html_resource.add_js_link(component.iife)

        if component.css:
            for css_link in component.css:
                html_resource.add_css_link(css_link)

        html_resource.add_vue_app_use(component.name)

    for plugin in system_slot._plugins:
        if not plugin.iife:
            continue

        html_resource.add_js_link(plugin.iife)

        if plugin.css:
            for css_link in plugin.css:
                html_resource.add_css_link(css_link)

        html_resource.add_vue_app_use(plugin.name)

    _css_file_link_to_style_code(html_resource)
    _js_file_link_to_script_code(html_resource)

    raw = render_zero_html(to_json())
    file.write_text(raw, "utf8")

    return file.resolve().absolute()


def _css_file_link_to_style_code(html_resource: HtmlResource):
    files = [link for link in html_resource._css_links.keys() if isinstance(link, Path)]

    for file in files:
        content = file.read_text(encoding="utf-8")
        html_resource.add_style_tag(content)

    # remove file links
    html_resource._css_links = {
        link: None
        for link in html_resource._css_links.keys()
        if not isinstance(link, Path)
    }


def _js_file_link_to_script_code(html_resource: HtmlResource):
    files = (
        info.link for info in html_resource._js_links if isinstance(info.link, Path)
    )

    for file in files:
        content = file.read_text(encoding="utf-8")
        html_resource.add_script_tag(content)

    # remove file links
    html_resource._js_links = [
        info for info in html_resource._js_links if not isinstance(info.link, Path)
    ]
