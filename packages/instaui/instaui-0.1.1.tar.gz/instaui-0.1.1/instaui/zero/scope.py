from instaui.runtime import new_app_slot, reset_app_slot
from contextlib import contextmanager


@contextmanager
def scope():
    token = new_app_slot("zero")
    yield
    reset_app_slot(token)
