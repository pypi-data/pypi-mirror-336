import inspect
from typing import Callable, Optional
from instaui.launch_collector import get_launch_collector, PageInfo


def page(
    url: str,
    *,
    page_loading: Optional[Callable] = None,
    use_tailwind: Optional[bool] = None,
):
    """Register a page route.

    Args:
        url (str): The route URL.
        page_loading (Optional[Callable], optional): Function to display a preload interface for the page. Defaults to None.
        use_tailwind (Optional[bool], optional): Whether to use tailwind or not. Defaults to None(not use tailwind).

    Raises:
        ValueError:  if page_loading_fn is a coroutine function
    """
    if page_loading is not None and inspect.iscoroutinefunction(page_loading):
        raise ValueError("page_loading_fn must be a synchronous function")

    def wrapper(func: Callable):
        get_launch_collector().register_page(
            PageInfo(url, func, page_loading, use_tailwind=use_tailwind)
        )
        return func

    return wrapper
