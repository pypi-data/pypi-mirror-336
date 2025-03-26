from instaui.runtime._app import get_current_scope
from instaui.vars.mixin_types.var_type import VarMixin


def register_var(object: VarMixin):
    """
    sid,id = register_var(object)
    """
    scope = get_current_scope()
    scope.register_var(object)

    return scope.id, scope.generate_vars_id()
