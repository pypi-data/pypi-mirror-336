from __future__ import annotations
from typing import (
    TypeVar,
)
from instaui.components.element import Element

_T = TypeVar("_T")


class Row(Element):
    def __init__(
        self,
    ):
        super().__init__("div")
        self.style("display: flex; flex-direction: row;")


    def gap(self, value: str) -> Row:
        return self.style({"gap": value})