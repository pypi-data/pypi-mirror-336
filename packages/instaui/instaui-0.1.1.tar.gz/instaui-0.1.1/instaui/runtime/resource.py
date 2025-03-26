from __future__ import annotations
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Optional, Set, Union
from .dataclass import JsLink, VueAppUse, VueAppComponent


class HtmlResource:
    _default_css_links: ClassVar[Dict[Union[str, Path], Any]] = {}
    _default_style_tags: ClassVar[List[str]] = []
    _default_js_links: ClassVar[List[JsLink]] = []
    _default_script_tags: ClassVar[List[str]] = []
    _default_vue_app_use: ClassVar[Set[VueAppUse]] = set()
    _default_vue_app_components: ClassVar[Set[VueAppComponent]] = set()
    use_tailwind: bool = False
    _title: str = ""

    def __init__(self) -> None:
        self._css_links: Dict[Union[str, Path], Any] = self._default_css_links.copy()
        self._style_tags: List[str] = self._default_style_tags.copy()
        self._js_links: List[JsLink] = self._default_js_links.copy()
        self._script_tags: List[str] = self._default_script_tags.copy()
        self._vue_app_use: Set[VueAppUse] = self._default_vue_app_use.copy()
        self._vue_app_components: Set[VueAppComponent] = (
            self._default_vue_app_components.copy()
        )
        self._import_maps: Dict[str, str] = {}
        self.title: str = self._title
        self._appConfig = "{}"

    def add_css_link(self, link: Union[str, Path]):
        self._css_links[link] = None

    def add_style_tag(self, content: str):
        self._style_tags.append(content)

    def add_js_link(
        self,
        link: Union[str, Path],
        *,
        attrs: Optional[Dict[str, Any]] = None,
        insert_before: int = -1,
    ):
        if insert_before == -1:
            self._js_links.append(JsLink(link, attrs or {}))
            return
        self._js_links.insert(insert_before, JsLink(link, attrs or {}))

    def add_script_tag(self, content: str):
        self._script_tags.append(content)

    def add_vue_app_use(self, name: str):
        self._vue_app_use.add(VueAppUse(name))

    def add_vue_app_component(self, name: str, url: str):
        self._vue_app_components.add(VueAppComponent(name, url))

    def add_import_map(self, name: str, link: str):
        self._import_maps[name] = link

    @classmethod
    def default_css_link(cls, link: Union[str, Path]):
        cls._default_css_links[link] = None

    @classmethod
    def default_style_tag(cls, content: str):
        cls._default_style_tags.append(content)

    @classmethod
    def default_js_link(
        cls,
        link: Union[str, Path],
        *,
        attrs: Optional[Dict[str, Any]] = None,
        insert_before: int = -1,
    ):
        if insert_before == -1:
            cls._default_js_links.append(JsLink(link, attrs or {}))
            return
        cls._default_js_links.insert(insert_before, JsLink(link, attrs or {}))

    @classmethod
    def default_script_tag(cls, content: str):
        cls._default_script_tags.append(content)

    @classmethod
    def default_vue_app_use(cls, name: str):
        cls._default_vue_app_use.add(VueAppUse(name))
