_active_input = None
_active_mouse = None
_active_window = None


def set_active_input(active_input):
    global _active_input
    _active_input = active_input


def get_input():
    return _active_input


def set_active_mouse(active_mouse):
    global _active_mouse
    _active_mouse = active_mouse


def get_mouse():
    return _active_mouse


def set_active_window(active_window):
    global _active_window
    _active_window = active_window


def get_window():
    return _active_window
