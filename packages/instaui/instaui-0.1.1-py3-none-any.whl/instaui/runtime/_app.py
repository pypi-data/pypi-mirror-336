from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Set
from instaui.common.jsonable import Jsonable
from .resource import HtmlResource
from instaui.consts import _T_App_Mode
from contextvars import ContextVar, Token
from copy import copy
from contextlib import contextmanager
from instaui.runtime.scope import Scope, GlobalScope
from types import MappingProxyType

if TYPE_CHECKING:
    from instaui.components.component import Component
    from instaui.components.slot import Slot
    from instaui.dependencies import ComponentRegistrationInfo, PluginRegistrationInfo
    from instaui.spa_router._route_model import RouteCollector


class App(Jsonable):
    _default_app_slot: ClassVar[Optional[App]] = None
    _default_js_components: ClassVar[Set[ComponentRegistrationInfo]] = set()
    _default_plugins: ClassVar[Set[PluginRegistrationInfo]] = set()

    def __init__(self, *, mode: _T_App_Mode) -> None:
        super().__init__()
        self._scope_id_counter = 0
        self._vfor_id_counter = 0
        self._slot_id_counter = 0
        self.mode: _T_App_Mode = mode
        self.items: List[Component] = []
        self._slots_stacks: List[Slot] = []

        defalut_scope = self.create_scope()
        self._scope_stack: List[Scope] = [defalut_scope]
        self._scopes: List[Scope] = [defalut_scope]
        self._html_resource = HtmlResource()
        self._js_components: Set[ComponentRegistrationInfo] = copy(
            self._default_js_components
        )

        self._plugins: Set[PluginRegistrationInfo] = copy(self._default_plugins)
        self._page_path: Optional[str] = None
        self._page_params: Dict[str, Any] = {}
        self._query_params: Dict[str, Any] = {}
        self._route_collector: Optional[RouteCollector] = None

    @property
    def page_path(self) -> str:
        assert self._page_path is not None, "Page path is not set"
        return self._page_path  # type: ignore

    @property
    def page_params(self):
        return MappingProxyType(self._page_params)

    @property
    def query_params(self):
        return MappingProxyType(self._query_params)

    def create_scope(self) -> Scope:
        self._scope_id_counter += 1
        scope = Scope(str(self._scope_id_counter))
        return scope

    def generate_vfor_id(self) -> str:
        self._vfor_id_counter += 1
        return str(self._vfor_id_counter)

    def generate_slot_id(self) -> str:
        self._slot_id_counter += 1
        return str(self._slot_id_counter)

    def reset_html_resource(self):
        self._html_resource = HtmlResource()

    def register_component(self, component: ComponentRegistrationInfo) -> None:
        self._js_components.add(component)

    def register_plugin(self, plugin: PluginRegistrationInfo) -> None:
        self._plugins.add(plugin)

    def register_router(self, collector: RouteCollector) -> None:
        self._route_collector = collector

    def append_component_to_container(self, component: Component):
        if self._slots_stacks:
            self._slots_stacks[-1]._children.append(component)
        else:
            self.items.append(component)

    def _to_json_dict(self):
        data = super()._to_json_dict()

        if self._page_path:
            url_info = {"path": self.page_path}
            if self._page_params:
                url_info["params"] = self._page_params  # type: ignore

            data["url"] = url_info

        assert len(self._scopes) == 1, "Only one scope is allowed"
        data["scope"] = self._scopes[0]

        if self._route_collector is not None:
            data["router"] = self._route_collector.model_dump(
                exclude_defaults=True, by_alias=True
            )

        return data

    @classmethod
    def _create_default(cls):
        if cls._default_app_slot is None:
            cls._default_app_slot = DefaultApp(mode="web")
        return cls._default_app_slot

    @classmethod
    def default_js_components(cls, component: ComponentRegistrationInfo):
        cls._default_js_components.add(component)

    @classmethod
    def default_plugins(cls, plugin: PluginRegistrationInfo):
        cls._default_plugins.add(plugin)


class DefaultApp(App):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DefaultApp, cls).__new__(cls)
        return cls._instance

    def create_scope(self) -> Scope:
        self._scope_id_counter += 1
        scope = GlobalScope(str(self._scope_id_counter))
        return scope

    def append_component_to_container(self, component: Component):
        raise ValueError("Operations are not allowed outside of ui.page")


_app_var: ContextVar[App] = ContextVar("_app_var", default=App._create_default())


def use_default_app_slot():
    assert App._default_app_slot is not None, "Default app slot is not set"
    _app_var.set(App._default_app_slot)


def get_default_app_slot():
    return App._create_default()


def get_app_slot() -> App:
    return _app_var.get()


def get_current_scope():
    current_scope = get_app_slot()._scope_stack[-1]
    if current_scope is None:
        raise ValueError("No current scope")
    return current_scope


@contextmanager
def new_scope(*, append_to_app: bool = True):
    app = get_app_slot()
    scope = app.create_scope()

    if append_to_app:
        app._scopes.append(scope)

    scope_stack = app._scope_stack
    scope_stack.append(scope)

    yield scope
    scope_stack.pop()


def get_slot_stacks():
    return get_app_slot()._slots_stacks


def pop_slot():
    get_slot_stacks().pop()


def new_app_slot(mode: _T_App_Mode):
    return _app_var.set(App(mode=mode))


def reset_app_slot(token: Token[App]):
    _app_var.reset(token)


def in_default_app_slot():
    return isinstance(get_app_slot(), DefaultApp)


def check_default_app_slot_or_error(
    error_message="Operations are not allowed outside of ui.page",
):
    if isinstance(get_app_slot(), DefaultApp):
        raise ValueError(error_message)
