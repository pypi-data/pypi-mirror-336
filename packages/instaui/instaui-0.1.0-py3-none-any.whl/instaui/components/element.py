from __future__ import annotations

import ast
from copy import copy
import inspect
from pathlib import Path
import re
from typing import (
    Any,
    Dict,
    List,
    ClassVar,
    Optional,
    Tuple,
    Union,
    overload,
    TYPE_CHECKING,
)
from typing_extensions import Self
from collections import defaultdict
from instaui.runtime._app import get_app_slot
from instaui.runtime._app import get_current_scope
from instaui.vars.element_ref import ElementRef


from instaui.vars.vfor_item import VForItem
from instaui.components.directive import Directive
from instaui.dependencies import ComponentRegistrationInfo, register_component
from .slot import SlotManager, Slot
from instaui import consts
from instaui.components.component import Component

from instaui.vars.mixin_types.element_binding import ElementBindingMixin

if TYPE_CHECKING:
    from instaui.event.event_mixin import EventMixin


# Refer to the NiceGUI project.
# https://github.com/zauberzeug/nicegui/blob/main/nicegui/element.py
PROPS_PATTERN = re.compile(
    r"""
# Match a key-value pair optionally followed by whitespace or end of string
([:\w\-]+)          # Capture group 1: Key
(?:                 # Optional non-capturing group for value
    =               # Match the equal sign
    (?:             # Non-capturing group for value options
        (           # Capture group 2: Value enclosed in double quotes
            "       # Match  double quote
            [^"\\]* # Match any character except quotes or backslashes zero or more times
            (?:\\.[^"\\]*)*  # Match any escaped character followed by any character except quotes or backslashes zero or more times
            "       # Match the closing quote
        )
        |
        (           # Capture group 3: Value enclosed in single quotes
            '       # Match a single quote
            [^'\\]* # Match any character except quotes or backslashes zero or more times
            (?:\\.[^'\\]*)*  # Match any escaped character followed by any character except quotes or backslashes zero or more times
            '       # Match the closing quote
        )
        |           # Or
        ([\w\-.%:\/]+)  # Capture group 4: Value without quotes
    )
)?                  # End of optional non-capturing group for value
(?:$|\s)            # Match end of string or whitespace
""",
    re.VERBOSE,
)


class Element(Component):
    component: ClassVar[Optional[ComponentRegistrationInfo]] = None
    _default_props: ClassVar[Dict[str, Any]] = {}
    _default_classes: ClassVar[List[str]] = []
    _default_style: ClassVar[Dict[str, str]] = {}

    def __init__(self, tag: Optional[Union[str, ElementBindingMixin]] = None):
        if self.component:
            tag = self.component.name

        super().__init__(tag)

        self._str_classes: List[str] = []
        self._dict_classes: Dict[str, ElementBindingMixin[bool]] = {}
        self._bind_str_classes: List[ElementBindingMixin[str]] = []
        self._str_classes.extend(self._default_classes)
        self._style: Dict[str, str] = {}
        self._style.update(self._default_style)
        self._style_str_binds: List[ElementBindingMixin[str]] = []
        self._props: Dict[str, Any] = {}
        self._props.update(self._default_props)
        self._proxy_props: List[ElementBindingMixin] = []

        self._js_events: defaultdict[str, List[EventMixin]] = defaultdict(list)
        self._web_events: defaultdict[str, List[EventMixin]] = defaultdict(list)
        self._directives: Dict[Directive, None] = {}

        self._slot_manager = SlotManager()
        self._element_ref: Optional[ElementRef] = None

    def __init_subclass__(
        cls,
        *,
        component: Union[str, Path, None] = None,
    ) -> None:
        super().__init_subclass__()

        if component:
            if isinstance(component, str):
                component = Path(component)
                if not component.is_absolute():
                    component = Path(inspect.getfile(cls)).parent / component

            # TODO: Lazy load component registration
            cls.component = register_component(
                component.stem, esm=component, shared=True
            )

        cls._default_props = copy(cls._default_props)
        cls._default_classes = copy(cls._default_classes)
        cls._default_style = copy(cls._default_style)

    @staticmethod
    def _update_classes(
        classes: List[str],
        add: str,
    ) -> List[str]:
        return list(dict.fromkeys(classes + add.split()))

    @staticmethod
    def _parse_style(text: Union[str, Dict[str, str]]) -> Dict[str, str]:
        if isinstance(text, dict):
            return text

        if not text:
            return {}

        result = {}
        for item in text.split(";"):
            item = item.strip()
            if item:
                key, value = item.split(":")
                key = key.strip()
                value = value.strip()
                result[key] = value

        return result

    @staticmethod
    def _parse_props(props: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(props, dict):
            return props

        if not props:
            return {}

        dictionary = {}
        for match in PROPS_PATTERN.finditer(props or ""):
            key = match.group(1)
            value = match.group(2) or match.group(3) or match.group(4)
            if value is None:
                dictionary[key] = True
            else:
                if (value.startswith("'") and value.endswith("'")) or (
                    value.startswith('"') and value.endswith('"')
                ):
                    value = ast.literal_eval(value)
                dictionary[key] = value
        return dictionary

    def key(self, key: Any):
        """Set the key prop of the component.

        Args:
            key (str): The key prop value.

        """
        self.props({"key": key})
        return self

    def vmodel(
        self,
        value: Any,
        modifiers: Union[consts.TModifier, List[consts.TModifier], None] = None,
        *,
        prop_name: str = "value",
        is_html_component=False,
    ):
        if prop_name == "value":
            prop_name = "modelValue"

        modifiers = modifiers or []
        if isinstance(modifiers, str):
            modifiers = [modifiers]

        self.directive(
            Directive(
                is_sys=is_html_component,
                name="vmodel",
                arg=prop_name,
                modifiers=modifiers,
                value=value,  # type: ignore
            )
        )

        if is_html_component is False:
            model_modifiers = {m: True for m in modifiers}
            self.props({"modelModifiers": model_modifiers})

        return self

    def add_slot(self, name: str) -> Slot:
        return self._slot_manager.get_slot(name)

    @overload
    def classes(self, add: str) -> Self: ...
    @overload
    def classes(self, add: Dict[str, ElementBindingMixin[bool]]) -> Self: ...

    @overload
    def classes(self, add: ElementBindingMixin[str]) -> Self: ...

    def classes(
        self,
        add: Union[
            str,
            Dict[str, ElementBindingMixin[bool]],
            ElementBindingMixin[str],
            VForItem,
        ],
    ) -> Self:
        if isinstance(add, str):
            self._str_classes = self._update_classes(self._str_classes, add)

        if isinstance(add, dict):
            self._dict_classes.update(**add)

        if isinstance(add, ElementBindingMixin):
            self._bind_str_classes.append(add)  # type: ignore

        return self

    def style(self, add: Union[str, Dict[str, Any], ElementBindingMixin[str]]) -> Self:
        if isinstance(add, dict):
            add = {key: value for key, value in add.items()}

        if isinstance(add, ElementBindingMixin):
            self._style_str_binds.append(add)
            return self

        new_style = self._parse_style(add)
        self._style.update(new_style)
        return self

    def props(self, add: Union[str, Dict[str, Any], ElementBindingMixin]) -> Self:
        if isinstance(add, ElementBindingMixin):
            self._proxy_props.append(add)
            return self

        if isinstance(add, dict):
            add = {key: value for key, value in add.items() if value is not None}
        new_props = self._parse_props(add)
        self._props.update(new_props)
        return self

    @classmethod
    def default_classes(cls, add: str) -> type[Self]:
        cls._default_classes = cls._update_classes(cls._default_classes, add)
        return cls

    @classmethod
    def default_style(cls, add: Union[str, Dict[str, str]]) -> type[Self]:
        new_style = cls._parse_style(add)
        cls._default_style.update(new_style)
        return cls

    @classmethod
    def default_props(cls, add: Union[str, Dict[str, Any]]) -> type[Self]:
        new_props = cls._parse_props(add)
        cls._default_props.update(new_props)
        return cls

    def on(
        self,
        event_name: str,
        handler: EventMixin,
        *,
        extends: Optional[List] = None,
    ):
        if extends:
            handler = handler.copy_with_extends(extends)

        if handler.event_type() == "js":
            self._js_events[event_name].append(handler)

        if handler.event_type() == "web":
            self._web_events[event_name].append(handler)

        return self

    def directive(self, directive: Directive) -> Self:
        self._directives[directive] = None
        return self

    def display(self, value: Union[ElementBindingMixin[bool], bool]) -> Self:
        return self.directive(Directive(is_sys=False, name="vshow", value=value))

    def event_dataset(self, data: Any, name: str = "event-data") -> Self:
        from instaui.vars.js_computed import JsComputed

        value = JsComputed(inputs=[data], code="(data)=> JSON.stringify(data)")
        self.props({f"data-{name}": value})
        return self

    def element_ref(self, ref: ElementRef):
        self._element_ref = ref
        return self

    def _to_json_dict(self):
        data = super()._to_json_dict()

        if self._style or self._style_str_binds:
            value_styles, bind_styles = _classifyBindableDict(self._style)
            if value_styles:
                data["style"] = value_styles

            b_style_list = []

            if bind_styles:
                b_style_list.append(bind_styles)

            if self._style_str_binds:
                b_style_list.append(
                    [v._to_element_binding_config() for v in self._style_str_binds]
                )

            if b_style_list:
                data["bStyle"] = b_style_list

        if self._str_classes or self._dict_classes or self._bind_str_classes:
            data["classes"] = _normalize_classes_data(
                self._str_classes, self._dict_classes, self._bind_str_classes
            )

        if self._props:
            value_props, bind_props = _classifyBindableDict(self._props)

            if value_props:
                data["props"] = value_props

            if bind_props:
                data["bProps"] = bind_props

        if self._proxy_props:
            data["proxyProps"] = [
                v._to_element_binding_config() for v in self._proxy_props
            ]

        if self._js_events or self._web_events:
            data["events"] = _normalize_events(self._js_events, self._web_events)

        if self._slot_manager.has_slot():
            data["slots"] = self._slot_manager

        if self._directives:
            data["dir"] = list(self._directives.keys())

        if self.component:
            get_app_slot().register_component(self.component)

        if self._element_ref:
            scope = get_current_scope()
            id = scope.generate_element_ref_id()
            self._element_ref._set_id(id)
            data["eRef"] = self._element_ref._to_element_config()
            scope.register_element_ref(self._element_ref)

        return data


def _normalize_events(
    js_events: defaultdict[str, List[EventMixin]],
    web_events: defaultdict[str, List[EventMixin]],
):
    merged: defaultdict[str, List[EventMixin]] = defaultdict(list)

    for name, events in js_events.items():
        name = _normalize_event_name(name)
        merged[name].extend(events)

    for name, events in web_events.items():
        name = _normalize_event_name(name)
        merged[name].extend(events)

    return dict(merged)


def _normalize_event_name(event_name: str):
    """'click' -> 'onClick' , 'press-enter' -> 'onPressEnter' , 'pressEnter' -> 'onPressEnter'"""

    if event_name.startswith("on-"):
        event_name = event_name[3:]

    if event_name.startswith("on"):
        event_name = event_name[2:]

    parts = event_name.split("-")
    formatted_parts = [part[0].upper() + part[1:] for part in parts]

    return "".join(["on", *formatted_parts])


def _normalize_classes_data(
    str_classes: List[str],
    dict_classes: Dict[str, ElementBindingMixin[bool]],
    bind_str_classes: List[ElementBindingMixin[str]],
):
    _str_result = " ".join(str_classes)

    _dict_classes = {k: v._to_element_binding_config() for k, v in dict_classes.items()}

    _bind_str_classes = [v._to_element_binding_config() for v in bind_str_classes]

    if _dict_classes or _bind_str_classes:
        result = {}

        if _str_result:
            result["str"] = _str_result

        if _dict_classes:
            result["map"] = _dict_classes

        if _bind_str_classes:
            result["bind"] = _bind_str_classes

        return result
    else:
        return _str_result


def _classifyBindableDict(
    data: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Return value_data, bind_data

    Args:
        data (Dict[str, Any]): _description_

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: _description_
    """

    value_data = {}
    bind_data = {}

    for key, value in data.items():
        if isinstance(value, ElementBindingMixin):
            bind_data[key] = value._to_element_binding_config()
        else:
            value_data[key] = value

    return value_data, bind_data
