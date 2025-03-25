from __future__ import annotations
from typing import (
    Any,
    Dict,
    Optional,
    Sequence,
    Union,
    cast,
)

from instaui.vars.mixin_types.observable import ObservableMixin

from . import _types
from . import _utils

from instaui.common.jsonable import Jsonable
from instaui.runtime._app import get_current_scope


class VueWatch(Jsonable):
    def __init__(
        self,
        sources: Union[Any, Sequence],
        callback: str,
        *,
        bindings: Optional[Dict[str, Any]] = None,
        immediate: bool = False,
        deep: Union[bool, int] = False,
        once: bool = False,
        flush: Optional[_types.TFlush] = None,
    ) -> None:
        get_current_scope().register_vue_watch(self)

        self.code = callback

        if isinstance(sources, Sequence):
            self.on = [
                cast(ObservableMixin, varObj)._to_observable_config()
                for varObj in sources
            ]
        else:
            self.on = cast(ObservableMixin, sources)._to_observable_config()

        if bindings:
            self.bind = {
                k: cast(ObservableMixin, v)._to_observable_config()
                for k, v in bindings.items()
            }

        if immediate is not False:
            self.immediate = immediate

        if deep is not False:
            _utils.assert_deep(deep)
            self.deep = deep

        if once is not False:
            self.once = once

        if flush is not None:
            self.flush = flush
