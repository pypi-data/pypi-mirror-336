from __future__ import annotations
from typing import (
    Any,
    Dict,
)

from instaui.common.jsonable import Jsonable
from instaui.vars.path_var import PathVar

from .mixin_types.var_type import VarMixin
from .mixin_types.py_binding import CanInputMixin, CanOutputMixin
from .mixin_types.element_binding import ElementBindingMixin
from .mixin_types.pathable import CanPathPropMixin
from .mixin_types.str_format_binding import StrFormatBindingMixin
from . import _utils


class ConstData(
    Jsonable,
    PathVar,
    VarMixin,
    CanInputMixin,
    CanOutputMixin,
    CanPathPropMixin,
    StrFormatBindingMixin,
    ElementBindingMixin,
):
    VAR_TYPE = "data"

    def __init__(self, value: Any = None) -> None:
        self.value = value  # type: ignore

        sid, id = _utils.register_var(self)
        self._sid = sid
        self._id = id

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

        return data


TConstData = ConstData
