from pygame.display import get_window_size as pg_win_get_size
from pygame.draw import rect as pg_draw_rect
from pygame.surface import SurfaceType
from pygex.image import AlphaSurface
from pygex.text import render_text
from time import time


_ANIMATION_DELAY = 0.25


_toast_start_time = -1
_toast_queue = []


class Toast:
    SHORT_DELAY = 2
    LONG_DELAY = 3.5

    def __init__(self, text, delay: float | int = SHORT_DELAY):
        self.text = text
        self.delay = delay

    def show(self):
        if self not in _toast_queue:
            _toast_queue.append(self)

        return self

    def cancel(self, animation=True):
        if self in _toast_queue:
            if self is _toast_queue[0]:
                global _toast_start_time

                if animation and time() - _toast_start_time < self.delay + _ANIMATION_DELAY:
                    _toast_start_time = time() - self.delay - _ANIMATION_DELAY
                    return

                _toast_start_time = -1

            _toast_queue.remove(self)


def render(surface: SurfaceType):
    if not _toast_queue:
        return

    current_time = time()

    global _toast_start_time

    if _toast_start_time == -1:
        _toast_start_time = current_time

    padding = 10
    toast = _toast_queue[0]
    text_surface = render_text(toast.text, 0xffffff)
    time_passed = current_time - _toast_start_time

    boxw, boxh = text_surface.get_size()
    boxw, boxh = boxw + padding * 2, boxh + padding * 2

    box_x, box_y = (pg_win_get_size()[0] - boxw) / 2, boxh - padding

    if time_passed <= _ANIMATION_DELAY:
        box_y = (box_y * 2 / _ANIMATION_DELAY) * time_passed - box_y
    elif time_passed >= _ANIMATION_DELAY + toast.delay:
        box_y -= (box_y * 2 / _ANIMATION_DELAY) * (time_passed - _ANIMATION_DELAY - toast.delay)

    box_surface = AlphaSurface((boxw, boxh))

    pg_draw_rect(box_surface, (0, 0, 0, 0xaa), (0, 0, boxw, boxh), 0, 5)

    surface.blit(box_surface, (box_x, box_y))
    surface.blit(text_surface, (box_x + padding, box_y + padding))

    if time_passed >= (toast.delay + _ANIMATION_DELAY * 2):
        del _toast_queue[0]
        _toast_start_time = -1


__all__ = 'Toast', 'render'
