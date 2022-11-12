from pygame import KEYDOWN, KEYUP, K_LCTRL, K_RCTRL, K_LALT, K_RALT
from pygame.event import Event


class Input:
    # Key statuses
    NOT_PRESSED = 0
    DOWN = 1
    HOLD = 2
    UP = 3

    # Keys
    K_MENU = 1073741925
    K_HOMEPAGE = 1073742093
    K_EMAIL = 1073742089
    K_MOVE_LEFT = 1073742094
    K_MOVE_RIGHT = 1073742095
    K_PLAY = 1073742085
    K_STOP = 1073742084
    K_VOLUME_UP = 1073741952
    K_VOLUME_DOWN = 1073741953
    K_NUMPAD_SLASH = 1073741908
    K_NUMPAD_ASTERISK = 1073741909
    K_NUMPAD_MINUS = 1073741910
    K_NUMPAD_PLUS = 1073741911
    K_NUMPAD_ENTER = 1073741912
    K_NUMPAD_0 = 1073741913
    K_NUMPAD_1 = 1073741914
    K_NUMPAD_2 = 1073741915
    K_NUMPAD_3 = 1073741916
    K_NUMPAD_4 = 1073741917
    K_NUMPAD_5 = 1073741918
    K_NUMPAD_6 = 1073741919
    K_NUMPAD_7 = 1073741920
    K_NUMPAD_8 = 1073741921
    K_NUMPAD_9 = 1073741922
    K_NUMPAD_DOT = 1073741923
    K_TILDA = 126
    K_PIPE = 124

    # Generalizing keys
    K_CTRL = -1
    K_ALT = -2

    def __init__(self):
        global _active_input
        _active_input = self

        self.key_data = {}

    def try_start_observing(self, key: int):
        if key >= 0:
            if key not in self.key_data:
                self.key_data[key] = Input.NOT_PRESSED

            return

        if key == Input.K_CTRL:
            if K_LCTRL not in self.key_data:
                self.key_data[K_LCTRL] = Input.NOT_PRESSED

            if K_RCTRL not in self.key_data:
                self.key_data[K_RCTRL] = Input.NOT_PRESSED
        elif key == Input.K_ALT:
            if K_LALT not in self.key_data:
                self.key_data[K_LALT] = Input.NOT_PRESSED

            if K_RALT not in self.key_data:
                self.key_data[K_RALT] = Input.NOT_PRESSED

    def get_status(self, key: int):
        self.try_start_observing(key)

        if key >= 0:
            return self.key_data[key]

        if key == Input.K_CTRL:
            return max(self.key_data[K_LCTRL], self.key_data[K_RCTRL])

        if key == Input.K_ALT:
            return max(self.key_data[K_LALT], self.key_data[K_RALT])

    def is_not_pressed(self, key: int):
        return self.get_status(key) == Input.NOT_PRESSED

    def is_down(self, key: int):
        return self.get_status(key) == Input.DOWN

    def is_hold(self, key: int):
        return self.get_status(key) == Input.HOLD

    def is_up(self, key: int):
        return self.get_status(key) == Input.UP

    def any_is_not_pressed(self, *keys: int):
        for key in keys:
            if self.get_status(key) == Input.NOT_PRESSED:
                return True

        return False

    def any_is_down(self, *keys: int):
        for key in keys:
            if self.get_status(key) == Input.DOWN:
                return True

        return False

    def any_is_hold(self, *keys: int):
        for key in keys:
            if self.get_status(key) == Input.HOLD:
                return True

        return False

    def any_is_up(self, *keys: int):
        for key in keys:
            if self.get_status(key) == Input.UP:
                return True

        return False

    def process_event(self, e: Event):
        if e.type == KEYDOWN and e.key in self.key_data:
            self.key_data[e.key] = Input.DOWN
        elif e.type == KEYUP and e.key in self.key_data:
            self.key_data[e.key] = Input.UP
    
    def flip(self):
        for key in self.key_data:
            if self.key_data[key] == Input.DOWN:
                self.key_data[key] = Input.HOLD
            elif self.key_data[key] == Input.UP:
                self.key_data[key] = Input.NOT_PRESSED


_active_input: Input | None = None


def get_input():
    return _active_input


__all__ = 'Input', 'get_input'
