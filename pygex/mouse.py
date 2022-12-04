from pygame.display import get_window_size as pg_win_get_size, get_desktop_sizes as pg_get_desktop_sizes
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEWHEEL, WINDOWMOVED
from pygame.mouse import get_pos as pg_mouse_get_pos, set_pos as pg_mouse_set_pos
from pygame.event import Event, set_grab
from pygex.input import Input
from typing import Sequence


class Mouse:
    FLAG_NO_BORDERS = 1 << 0
    FLAG_CONFINED = 1 << 1
    FLAG_CAPTURED = 1 << 2

    def __init__(self):
        global _active_mouse
        _active_mouse = self

        self._last_pos = pg_mouse_get_pos()

        # ABOUT THIS VARIABLE:
        # - the window position is necessary for `flip()` function to prevent a bug related
        # to the difference between the maximum mouse position and the maximum position
        # to the right or bottom of the window
        # - the window initially appears in the center (by default)
        # - storing and retrieving the window position separately in this class is necessary
        # to avoid recursions with the module `window.py`
        self._win_pos = pg_get_desktop_sizes()[0]
        self._win_pos = (self._win_pos[0] - pg_win_get_size()[0]) // 2, (self._win_pos[1] - pg_win_get_size()[1]) // 2

        self.flags = 0

        self.button_statuses = [Input.NOT_PRESSED] * 3
        self.wheel = (0, 0)

    @property
    def left_is_not_pressed(self):
        return self.button_statuses[0] == Input.NOT_PRESSED

    @property
    def left_is_down(self):
        return self.button_statuses[0] == Input.DOWN

    @property
    def left_is_hold(self):
        return self.button_statuses[0] == Input.HOLD

    @property
    def left_is_up(self):
        return self.button_statuses[0] == Input.UP

    @property
    def middle_is_not_pressed(self):
        return self.button_statuses[1] == Input.NOT_PRESSED

    @property
    def middle_is_down(self):
        return self.button_statuses[1] == Input.DOWN

    @property
    def middle_is_hold(self):
        return self.button_statuses[1] == Input.HOLD

    @property
    def middle_is_up(self):
        return self.button_statuses[1] == Input.UP

    @property
    def right_is_not_pressed(self):
        return self.button_statuses[2] == Input.NOT_PRESSED

    @property
    def right_is_down(self):
        return self.button_statuses[2] == Input.DOWN

    @property
    def right_is_hold(self):
        return self.button_statuses[2] == Input.HOLD

    @property
    def right_is_up(self):
        return self.button_statuses[2] == Input.UP

    @property
    def is_wheel_up(self):
        return self.wheel[0] > 0

    @property
    def is_wheel_down(self):
        return self.wheel[0] < 0

    @property
    def is_wheel(self):
        return self.wheel != (0, 0)

    @property
    def is_moved(self):
        return self.rel != (0, 0)

    @property
    def relx(self):
        return self._last_pos[0] - pg_mouse_get_pos()[0]

    @property
    def rely(self):
        return self._last_pos[1] - pg_mouse_get_pos()[1]

    @property
    def rel(self):
        return self.relx, self.rely

    @property
    def pos(self):
        return pg_mouse_get_pos()

    @pos.setter
    def pos(self, value: Sequence[int]):
        pg_mouse_set_pos(value)

    @property
    def x(self):
        return pg_mouse_get_pos()[0]

    @x.setter
    def x(self, value: int):
        pg_mouse_set_pos(value, pg_mouse_get_pos()[1])

    @property
    def y(self):
        return pg_mouse_get_pos()[1]

    @y.setter
    def y(self, value: int):
        pg_mouse_set_pos(pg_mouse_get_pos()[0], value)

    def add_flags(self, flags: int):
        self.flags |= flags

    def remove_flags(self, flags: int):
        self.flags &= ~flags

    def process_event(self, e: Event):
        if e.type == MOUSEWHEEL:
            self.wheel = (e.x, e.y)

        event_types = (MOUSEBUTTONDOWN, MOUSEBUTTONUP)
        statuses = (Input.DOWN, Input.UP)

        for i in range(2):
            if e.type == event_types[i]:
                for k in range(len(self.button_statuses)):
                    if e.button == k + 1:
                        self.button_statuses[k] = statuses[i]

        if e.type == WINDOWMOVED:
            self._win_pos = e.x, e.y

    def flip(self):
        set_grab(bool(self.flags & Mouse.FLAG_CONFINED))

        if self.flags & Mouse.FLAG_NO_BORDERS:
            winw, winh = pg_win_get_size()
            desktopw, desktoph = pg_get_desktop_sizes()[0]

            offset_x = offset_y = 0

            # ABOUT THIS TWO CONDITIONS:
            # - when the right or bottom of the window becomes adjacent to the right or bottom of the desktop
            # the difference between these values and the maximum mouse position is 6
            if self._win_pos[0] >= desktopw - winw - 5:
                offset_x = 6

            if self._win_pos[1] >= desktoph - winh - 5:
                offset_y = 6

            if self.x > winw - offset_x:
                self.x = 0
            elif self.x <= 0:
                self.x = winw

            if self.y > winh - offset_y:
                self.y = 0
            elif self.y <= 0:
                self.y = winh

        for i in range(len(self.button_statuses)):
            if self.button_statuses[i] == Input.DOWN:
                self.button_statuses[i] = Input.HOLD
            elif self.button_statuses[i] == Input.UP:
                self.button_statuses[i] = Input.NOT_PRESSED

        self.wheel = (0, 0)
        self._last_pos = pg_mouse_get_pos()

        if self.flags & Mouse.FLAG_CAPTURED:
            pg_mouse_set_pos(pg_win_get_size()[0] / 2, pg_win_get_size()[1] / 2)


_active_mouse: Mouse | None = None


def get_mouse():
    return _active_mouse


__all__ = 'Mouse', 'get_mouse'
