from .component_registrar import (
    ComponentRegistrationInfo,
    register_component,
    PluginRegistrationInfo,
    register_plugin,
)
from .installer import install_component

__all__ = [
    "ComponentRegistrationInfo",
    "register_component",
    "PluginRegistrationInfo",
    "register_plugin",
    "install_component",
]
