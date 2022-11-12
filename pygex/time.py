from time import time


class Clock:
    def __init__(self):
        global _active_clock
        _active_clock = self

        self._timers = {}

    def time_has_passed(self, milliseconds: int):
        if milliseconds in self._timers:
            return time() - self._timers[milliseconds] >= milliseconds / 1000

        self._timers[milliseconds] = time()

    def reset_timer(self, milliseconds: int):
        self._timers[milliseconds] = time()

    def flip(self):
        for milliseconds in self._timers:
            if time() - self._timers[milliseconds] >= milliseconds / 1000:
                self._timers[milliseconds] = time()


_active_clock: Clock | None = None


def get_clock():
    return _active_clock


__all__ = 'Clock', 'get_clock'
