from pygame.display import flip as pg_flip, get_surface as get_display_surface, init as display_init
from pygex.mouse import Mouse, get_mouse
from pygex.input import Input, get_input
from pygex.color import colorValue
from pygame.constants import QUIT
from pygame.event import Event
from pygame.time import Clock


display_init()

_mouse = Mouse()
_input = Input()
_pg_clock = Clock()


def get_clock():
    return _pg_clock


def process_event(e: Event, default_quit=True):
    if default_quit and e.type == QUIT:
        exit()

    _mouse.process_event(e)
    _mouse.process_event(e)


def flip(bg_color: colorValue | None = None, fps_limit: float | None = None):
    pg_flip()
    _mouse.flip()
    _input.flip()

    if bg_color is not None:
        get_display_surface().fill(bg_color)

    if fps_limit is not None:
        _pg_clock.tick(fps_limit)


__all__ = 'Input', 'get_input', 'get_mouse', 'get_clock', 'process_event', 'flip'
