from __future__ import annotations
from typing import Callable, Optional, TYPE_CHECKING
from dataclasses import dataclass
from urllib.parse import quote


if TYPE_CHECKING:
    from instaui.runtime.resource import HtmlResource


@dataclass
class PageInfo:
    path: str
    func: Callable
    page_loading: Optional[Callable] = None
    use_tailwind: Optional[bool] = None

    def create_key(self) -> str:
        return quote(self.path)

    def apply_settings(self, html_resource: HtmlResource):
        if self.use_tailwind is not None:
            html_resource.use_tailwind = self.use_tailwind
