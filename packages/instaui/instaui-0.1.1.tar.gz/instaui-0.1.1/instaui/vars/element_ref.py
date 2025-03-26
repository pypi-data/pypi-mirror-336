from __future__ import annotations
from instaui.common.jsonable import Jsonable
from instaui.runtime._app import get_current_scope
from instaui.vars.mixin_types.py_binding import CanOutputMixin


class ElementRef(Jsonable, CanOutputMixin):
    def __init__(self) -> None:
        self._id = None
        self.__sid = get_current_scope().id

    def _set_id(self, id: str):
        self._id = id

    def __to_binding_config(
        self,
    ):
        return {
            "type": "ele_ref",
            "id": self._id,
            "sid": self.__sid,
        }

    def _to_output_config(self):
        return self.__to_binding_config()

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["id"] = self._id
        data["sid"] = self.__sid

        return data

    def _to_element_config(self):
        return {"id": self._id, "sid": self.__sid}


def run_element_method(method_name: str, *args, **kwargs):
    return {
        "method": method_name,
        "args": args,
    }
