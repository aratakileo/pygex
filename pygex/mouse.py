from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEWHEEL
from pygame.mouse import get_pos as pg_mouse_get_pos
from pygame.event import Event
from pygex.input import Input


class Mouse:
    def __init__(self):
        global _active_mouse
        _active_mouse = self

        self._last_pos = pg_mouse_get_pos()

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

    get_pos = pg_mouse_get_pos

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

    def flip(self):
        for i in range(len(self.button_statuses)):
            if self.button_statuses[i] == Input.DOWN:
                self.button_statuses[i] = Input.HOLD
            elif self.button_statuses[i] == Input.UP:
                self.button_statuses[i] = Input.NOT_PRESSED

        self.wheel = (0, 0)
        self._last_pos = pg_mouse_get_pos()


_active_mouse: Mouse | None = None


def get_mouse():
    return _active_mouse


__all__ = 'Mouse', 'get_mouse'
