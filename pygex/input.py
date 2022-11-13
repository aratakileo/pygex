from pygame import (
    KEYDOWN, KEYUP, K_LCTRL, K_RCTRL, K_LALT, K_RALT, K_RETURN, K_KP_ENTER, K_KP_PERIOD, K_PERIOD, K_LSHIFT, K_RSHIFT
)
from pygame.event import Event
from time import time


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
    K_KP_RETURN = K_KP_ENTER
    K_KP_DOT = K_KP_PERIOD
    K_TILDA = 126
    K_PIPE = 124
    K_DOT = K_PERIOD

    # Generalizing keys
    GK_CTRL = 'CTRL'
    GK_ALT = 'ALT'
    GK_SHIFT = 'SHIFT'
    GK_ENTER = 'ENTER'

    # Hold duration
    FIRST_HOLD_DURATION = 0.5
    HOLD_DURATION = 0.1

    def __init__(self):
        global _active_input
        _active_input = self

        self._keys_data = {}
        self._generalized_keys = {}

        self.generalize_keys(Input.GK_CTRL, K_LCTRL, K_RCTRL)
        self.generalize_keys(Input.GK_ALT, K_LALT, K_RALT)
        self.generalize_keys(Input.GK_SHIFT, K_LSHIFT, K_RSHIFT)
        self.generalize_keys(Input.GK_ENTER, K_RETURN, K_KP_ENTER)

    def reset(self, key: int):
        self._keys_data[key] = [Input.NOT_PRESSED, -1, True]

    def generalize_keys(self, name: str, *keys: int | str):
        self._generalized_keys[name] = ()

        for key in keys:
            if isinstance(key, int):
                self._generalized_keys[name] = *self._generalized_keys[name], key
                continue

            self._generalized_keys[name] = *self._generalized_keys[name], self._generalized_keys[key]

    def try_start_observing(self, key: int | str):
        if isinstance(key, int):
            if key not in self._keys_data:
                self.reset(key)

            return

        for _key in self._generalized_keys[key]:
            if _key not in self._keys_data:
                self.reset(_key)

    def get_status(self, key: int | str):
        self.try_start_observing(key)

        if isinstance(key, int):
            return self._keys_data[key][0]

        return max(tuple(self._keys_data[_key][0] for _key in self._generalized_keys[key]))

    def __get_time(self, key: int | str):
        if isinstance(key, int):
            return self._keys_data[key][1]

        return max(tuple(self._keys_data[_key][1] for _key in self._generalized_keys[key]))

    def __is_hold_first_time(self, key: int | str):
        if isinstance(key, int):
            return self._keys_data[key][2]

        return bool(sum(tuple(self._keys_data[_key][2] for _key in self._generalized_keys[key])))

    def is_not_pressed(self, key: int | str):
        return self.get_status(key) == Input.NOT_PRESSED

    def is_down(self, key: int | str):
        return self.get_status(key) == Input.DOWN

    def is_hold(self, key: int | str):
        return self.get_status(key) == Input.HOLD

    def is_up(self, key: int | str):
        return self.get_status(key) == Input.UP

    def is_applying(self, key: int | str, no_reset=False):
        self.try_start_observing(key)

        current_time = time()
        dt = current_time - self.__get_time(key)
        is_hold_first_time = self.__is_hold_first_time(key)
        hold_duration = Input.FIRST_HOLD_DURATION if is_hold_first_time else Input.HOLD_DURATION

        if self.is_up(key) and dt < hold_duration and is_hold_first_time:
            return True

        if self.is_hold(key) and dt >= hold_duration:
            if isinstance(key, int):
                if not no_reset:
                    self._keys_data[key][1:] = [current_time, False]

                return True

            for _key in self._generalized_keys[key]:
                if not no_reset:
                    self._keys_data[_key][1:] = [current_time, False]

            return True

        return False

    def any_is_not_pressed(self, *keys: int | str):
        for key in keys:
            if self.get_status(key) == Input.NOT_PRESSED:
                return True

        return False

    def any_is_down(self, *keys: int | str):
        for key in keys:
            if self.get_status(key) == Input.DOWN:
                return True

        return False

    def any_is_hold(self, *keys: int | str):
        for key in keys:
            if self.get_status(key) == Input.HOLD:
                return True

        return False

    def any_is_up(self, *keys: int | str):
        for key in keys:
            if self.get_status(key) == Input.UP:
                return True

        return False

    def any_is_applying(self, *keys: int | str, no_reset=False):
        for key in keys:
            if self.is_applying(key, no_reset):
                return True

        return False

    def process_event(self, e: Event):
        if e.type == KEYDOWN and e.key in self._keys_data:
            self._keys_data[e.key][0] = Input.DOWN
        elif e.type == KEYUP and e.key in self._keys_data:
            self._keys_data[e.key][0] = Input.UP

    def flip(self):
        for key in self._keys_data:
            if self._keys_data[key][0] == Input.DOWN:
                self._keys_data[key][:-1] = [Input.HOLD, time()]
            elif self._keys_data[key][0] == Input.UP:
                self.reset(key)


_active_input: Input | None = None


def get_input():
    return _active_input


__all__ = 'Input', 'get_input'
