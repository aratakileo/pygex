from pygex.input import Input
from pygex.mouse import Mouse
from pygex.window import Window


def set_active_input(active_input: Input): ...

def get_input() -> Input: ...

def set_active_mouse(active_mouse: Mouse): ...

def get_mouse() -> Mouse: ...

def set_active_window(active_mouse: Window): ...

def get_window() -> Window: ...


__all__ = 'get_input', 'get_mouse', 'get_window'
