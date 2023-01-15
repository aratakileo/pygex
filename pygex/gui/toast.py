from pygex.color import COLOR_TYPE, to_pygame_alpha_color, to_readable_color
from pygame.display import get_window_size as pg_win_get_size
from pygame.draw import rect as pg_draw_rect
from pygame.surface import SurfaceType
from pygex.image import AlphaSurface
from pygex.text import render_text
from typing import Sequence
from time import time


class Toast:
    SHORT_DELAY = 2
    LONG_DELAY = 3.5

    def __init__(self, text, delay: float | int = SHORT_DELAY):
        self.text = text
        self.delay = delay

        self.animation_delay = 0.25
        self.padding = 10
        self.text_color: COLOR_TYPE = ...
        self.bg_color: COLOR_TYPE = 0xaa000000
        self.border_radius_or_radii: int | Sequence[int] = 5

    def show(self):
        if self not in _toast_queue:
            _toast_queue.append(self)

        return self

    def cancel(self, animation=True):
        if self in _toast_queue:
            if self is _toast_queue[0]:
                global _toast_start_time

                if animation and time() - _toast_start_time < self.delay + self.animation_delay:
                    _toast_start_time = time() - self.delay - self.animation_delay
                    return

                _toast_start_time = -1

            _toast_queue.remove(self)


_toast_start_time = -1
_toast_queue: list[Toast] = []


def render(surface: SurfaceType):
    if not _toast_queue:
        return

    current_time = time()

    global _toast_start_time

    if _toast_start_time == -1:
        _toast_start_time = current_time

    toast = _toast_queue[0]
    text_color = toast.text_color if toast.text_color is not ... else to_readable_color(toast.bg_color)
    text_surface = render_text(toast.text, text_color)
    time_passed = current_time - _toast_start_time

    boxw, boxh = text_surface.get_size()
    boxw, boxh = boxw + toast.padding * 2, boxh + toast.padding * 2

    box_x, box_y = (pg_win_get_size()[0] - boxw) / 2, boxh - toast.padding

    if time_passed <= toast.animation_delay:
        box_y = (box_y * 2 / toast.animation_delay) * time_passed - box_y
    elif time_passed >= toast.animation_delay + toast.delay:
        box_y -= (box_y * 2 / toast.animation_delay) * (time_passed - toast.animation_delay - toast.delay)

    box_surface = AlphaSurface((boxw, boxh))

    border_radii = (toast.border_radius_or_radii,) if isinstance(toast.border_radius_or_radii, int) \
        else (-1, *toast.border_radius_or_radii)

    pg_draw_rect(box_surface, to_pygame_alpha_color(toast.bg_color), (0, 0, boxw, boxh), 0, *border_radii)

    surface.blit(box_surface, (box_x, box_y))
    surface.blit(text_surface, (box_x + toast.padding, box_y + toast.padding))

    if time_passed >= (toast.delay + toast.animation_delay * 2):
        del _toast_queue[0]
        _toast_start_time = -1


__all__ = 'Toast', 'render'
