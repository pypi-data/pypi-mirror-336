from __future__ import annotations
from typing import (
    Literal,
    Optional,
    TypeVar,
    Union,
)
from instaui.vars.types import TMaybeRef
from instaui.vars.js_computed import JsComputed
from instaui.components.element import Element
from instaui.vars.mixin_types.observable import ObservableMixin

_T = TypeVar("_T")


class Grid(Element):
    def __init__(
        self,
        rows: Optional[TMaybeRef[Union[int, str]]] = None,
        columns: Optional[TMaybeRef[Union[int, str]]] = None,
    ):
        super().__init__("div")
        self.style("display: grid;")

        if rows is not None:
            if isinstance(rows, int):
                rows = f"repeat({rows}, 1fr)"

            if isinstance(rows, ObservableMixin):
                rows = _convert_to_repeat_computed(rows)

            self.style({"grid-template-rows": rows})

        if columns is not None:
            if isinstance(columns, int):
                columns = f"repeat({columns}, 1fr)"

            if isinstance(columns, ObservableMixin):
                columns = _convert_to_repeat_computed(columns)

            self.style({"grid-template-columns": columns})

    @classmethod
    def auto_columns(
        cls,
        *,
        min_width: TMaybeRef[str],
        mode: TMaybeRef[Literal["auto-fill", "auto-fit"]] = "auto-fit",
    ) -> Grid:
        if isinstance(min_width, ObservableMixin) or isinstance(mode, ObservableMixin):
            template = JsComputed(
                inputs=[min_width, mode],
                code=r"(min_width, mode)=> `repeat(${mode}, minmax(min(${min_width},100%), 1fr))`",
            )

        else:
            template = f"repeat({mode}, minmax(min({min_width},100%), 1fr))"

        return cls(columns=template)

    def row_gap(self, gap: TMaybeRef[str]) -> Grid:
        return self.style({"row-gap": gap})

    def column_gap(self, gap: TMaybeRef[str]) -> Grid:
        return self.style({"column-gap": gap})

    def gap(self, gap: TMaybeRef[str]) -> Grid:
        return self.row_gap(gap).column_gap(gap)


def _convert_to_repeat_computed(value: ObservableMixin):
    return JsComputed(
        inputs=[value],
        code=r"""(value)=> {
    if (typeof value === "number"){
        return `repeat(${value}, 1fr)`
    }
    return value                     
    }""",
    )
