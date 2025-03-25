from __future__ import annotations
from typing import (
    Generic,
    List,
    Optional,
    Union,
    TypeVar,
)
from instaui.components.element import Element
from instaui import consts

from instaui.vars.types import TMaybeRef
from instaui.vars.web_computed import WebComputed


_T = TypeVar("_T")


class ValueElement(Element, Generic[_T]):
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Union[_T, TMaybeRef[_T], None] = None,
        is_html_component: bool = False,
        value_name: str = "value",
    ):
        super().__init__(tag)
        self.__is_html_component = is_html_component

        if value is not None:
            if isinstance(value, WebComputed):
                self.props({value_name:value})
            else:
                self.vmodel(value, prop_name=value_name)

    def vmodel(
        self,
        value,
        modifiers: Union[consts.TModifier, List[consts.TModifier], None] = None,
        *,
        prop_name: str = "value",
    ):
        return super().vmodel(
            value,
            modifiers,
            prop_name=prop_name,
            is_html_component=self.__is_html_component,
        )
