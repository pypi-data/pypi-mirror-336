import inspect
from pathlib import Path
from typing import List, Optional, Type, Union
from instaui.systems.file_system import generate_hash_name_from_path
from dataclasses import dataclass, field
from instaui.runtime import get_app_slot
from instaui.runtime._app import App


class ComponentRegistrar:
    def __init__(self, js_file: Path):
        self.js_file = js_file
        self.key = f"{generate_hash_name_from_path(js_file.parent)}/{js_file.name}"
        self.name = js_file.stem

    def __hash__(self) -> int:
        return hash(self.js_file)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ComponentRegistrar):
            return False
        return self.js_file == other.js_file

    @classmethod
    def create(cls, js_file: Union[str, Path], target_class: Type):
        js_file = Path(js_file)
        base = Path(inspect.getfile(target_class)).parent
        if not js_file.is_absolute():
            js_file = base / js_file
        return cls(js_file)


@dataclass(frozen=True)
class ComponentRegistrationInfo:
    name: str
    esm: Optional[Path] = None
    iife: Optional[Path] = None
    css: List[Path] = field(default_factory=list, compare=False)


@dataclass(frozen=True)
class PluginRegistrationInfo:
    name: str
    esm: Optional[Path] = None
    iife: Optional[Path] = None
    css: List[Path] = field(default_factory=list, compare=False)


def register_plugin(
    name: str,
    esm: Optional[Path] = None,
    iife: Optional[Path] = None,
    css: Optional[Union[Path, List[Path]]] = None,
    shared: bool = False,
):
    css = [css] if isinstance(css, Path) else css

    cr = PluginRegistrationInfo(name, esm, iife, css or [])

    if shared:
        App.default_plugins(cr)

    get_app_slot().register_plugin(cr)
    return cr


def register_component(
    name: str,
    esm: Optional[Path] = None,
    iife: Optional[Path] = None,
    css: Optional[Union[Path, List[Path]]] = None,
    shared: bool = False,
):
    css = [css] if isinstance(css, Path) else css

    cr = ComponentRegistrationInfo(f"instaui-{name}", esm, iife, css or [])

    if shared:
        App.default_js_components(cr)

    get_app_slot().register_component(cr)
    return cr
