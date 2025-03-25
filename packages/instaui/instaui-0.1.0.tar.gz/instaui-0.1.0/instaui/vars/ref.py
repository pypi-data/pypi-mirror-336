from __future__ import annotations
from typing import (
    Dict,
    Generic,
    Optional,
    TypeVar,
    Union,
    overload,
)

from instaui.common.jsonable import Jsonable
from instaui.vars.path_var import PathVar

from .mixin_types.var_type import VarMixin
from .mixin_types.py_binding import CanInputMixin, CanOutputMixin
from .mixin_types.observable import ObservableMixin
from .mixin_types.element_binding import ElementBindingMixin
from .mixin_types.pathable import CanPathPropMixin
from .mixin_types.str_format_binding import StrFormatBindingMixin
from . import _utils


_T_Value = TypeVar("_T_Value")


class Ref(
    Jsonable,
    PathVar,
    VarMixin,
    ObservableMixin,
    CanInputMixin,
    CanOutputMixin,
    CanPathPropMixin,
    StrFormatBindingMixin,
    ElementBindingMixin[_T_Value],
    Generic[_T_Value],
):
    VAR_TYPE = "ref"

    def __init__(self, value: Optional[_T_Value] = None) -> None:
        self.value = value  # type: ignore

        sid, id = _utils.register_var(self)
        self._sid = sid
        self._id = id
        self._debounced = None

    def debounced(self, secounds: float):
        self._debounced = secounds
        return self

    def __to_binding_config(self):
        return {
            "type": self.VAR_TYPE,
            "id": self._id,
            "sid": self._sid,
        }

    def _to_pathable_binding_config(self) -> Dict:
        return self.__to_binding_config()

    def _to_path_prop_binding_config(self) -> Dict:
        return self.__to_binding_config()

    def _to_observable_config(self):
        return self.__to_binding_config()

    def _to_input_config(self):
        return self.__to_binding_config()

    def _to_output_config(self):
        return self.__to_binding_config()

    def _to_element_binding_config(self):
        return self.__to_binding_config()

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["sid"] = self._sid
        data["id"] = self._id
        data["type"] = self.VAR_TYPE

        if self._debounced is not None:
            data["debounced"] = self._debounced

        return data


TRef = Ref


@overload
def ref(value: Ref[_T_Value]) -> Ref[_T_Value]: ...


@overload
def ref(value: Optional[_T_Value] = None) -> Ref[_T_Value]: ...


def ref(value: Union[Ref[_T_Value], _T_Value, None] = None):
    if isinstance(value, Ref):
        return value
    return Ref(value)
