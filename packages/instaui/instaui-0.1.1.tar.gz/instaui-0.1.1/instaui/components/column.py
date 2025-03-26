from __future__ import annotations
from typing import Literal
from instaui.components.element import Element
from instaui.vars.types import TMaybeRef


class Column(Element):
    def __init__(self):
        super().__init__("div")
        self.style("display: flex; flex-direction: column;gap:var(--insta-column-gap)")

    def gap(self, value: TMaybeRef[str]) -> Column:
        return self.style({"gap": value})

    def align_items(
        self, value: TMaybeRef[Literal["start", "end", "center", "stretch", "revert"]]
    ) -> Column:
        return self.style({"align-items": value})
