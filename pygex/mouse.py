from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEWHEEL
from pygame.mouse import get_pos, get_rel
from pygame.event import Event
from pygex.input import Input


class Mouse:
    def __init__(self):
        global _active_mouse
        _active_mouse = self

        self.button_statuses = [Input.NOT_PRESSED] * 3
        self.mouse_wheel = (0, 0)
        self.get_pos = get_pos

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
        return self.mouse_wheel[0] > 0

    @property
    def is_wheel_down(self):
        return self.mouse_wheel[0] < 0

    @property
    def is_moved(self):
        return self.relative != (0, 0)
    
    @property
    def relative(self):
        return get_rel()

    def process_event(self, e: Event):
        if e.type == MOUSEWHEEL:
            self.mouse_wheel = (e.x, e.y)

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

        self.mouse_wheel = (0, 0)


_active_mouse: Mouse | None = None


def get_mouse():
    return _active_mouse


__all__ = 'Mouse', 'get_mouse'
