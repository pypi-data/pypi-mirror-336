from instaui.runtime.context import get_context


def create_server(
    debug: bool = True,
):
    from instaui.fastapi_server.server import Server

    context = get_context()
    context._app_mode = "web"
    context._debug_mode = debug

    return Server.get_instance()
