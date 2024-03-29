from pygame.display import set_mode as pg_win_set_mode, set_caption as pg_win_set_caption, flip as pg_display_flip
from pygame.display import get_surface as pg_win_get_surface, get_window_size as pg_win_get_size
from pygame.display import get_caption as pg_win_get_caption, init as pg_display_init
from pygame.constants import QUIT, FULLSCREEN, RESIZABLE, WINDOWMOVED
from pygex.core.broker import set_active_window, get_mouse, get_input
from pygame.display import get_desktop_sizes as pg_get_desktop_sizes
from pygex.gui.toast import Toast, render as render_toasts
from pygex.core.interface import Flippable, Renderable
from pygame.mouse import get_pos as pg_mouse_get_pos
from pygame.image import save as pg_save_image
from pygame.event import get as get_events
from pygame.time import Clock as pg_Clock
from pygame.base import quit as pg_quit
from pygex.color import TYPE_COLOR
from pygame.event import Event
from pygex.input import Input
from pygex.mouse import Mouse
from datetime import datetime
from typing import Sequence
from os.path import isdir
from os import makedirs
from time import time


class Window(Flippable):
    def __init__(
            self,
            size: Sequence[int] = (800, 600),
            title='Pygex window',
            fps_limit: float | int | None = None,
            fullscreen=False,
            resizable=True,
            vsync=False,
            flags=0
    ):
        set_active_window(self)
        pg_display_init()
        pg_win_set_mode(size, flags | RESIZABLE * resizable, vsync=vsync)
        pg_win_set_caption(title)

        if get_mouse() is None:
            Mouse()

        if get_input() is None:
            Input()

        self._flippable_list: list[Flippable] = []
        self._renderable_list: list[Renderable] = []
        self._view_list = []
        self._event_buffer = []

        self._clock = pg_Clock()
        self._fps_counter_start_time = self._last_frame_time = time()
        self._fps_counter_num = 0
        self._fps_num = 60
        self._dt = 0

        self._size = *size,
        self._vsync = vsync

        self._pos = pg_get_desktop_sizes()[0]
        self._pos = (self._pos[0] - self._size[0]) // 2, (self._pos[1] - self._size[1]) // 2

        self._is_running = True

        self.hold_event_buffer = False
        self.default_quit = True
        self.fps_limit = fps_limit
        self.bg_color: TYPE_COLOR | None = None

        if fullscreen:
            self.fullscreen = True

    @property
    def title(self):
        return pg_win_get_caption()[0]

    @title.setter
    def title(self, value: str):
        pg_win_set_caption(value)

    @property
    def size(self):
        return pg_win_get_size() if not self.fullscreen else pg_get_desktop_sizes()[0]

    @size.setter
    def size(self, value: Sequence):
        if not self.fullscreen:
            self._size = *value,
            pg_win_set_mode(value, pg_win_get_surface().get_flags(), vsync=self._vsync)

    @property
    def width(self):
        return self.size[0]

    @width.setter
    def width(self, value: int):
        self.size = value, self.size[0]

    @property
    def height(self):
        return self.size[1]

    @height.setter
    def height(self, value: int):
        self.size = self.size[0], value

    @property
    def pos(self) -> tuple[int, int]:
        return (0, 0) if pg_win_get_surface().get_flags() & FULLSCREEN else self._pos

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def mouse(self):
        return get_mouse()

    @property
    def input(self):
        return get_input()

    @property
    def clock(self):
        return self._clock

    @property
    def surface(self):
        return pg_win_get_surface()

    @property
    def fps(self):
        return self._fps_num if self.fps_limit is None else self._clock.get_fps()

    @property
    def flags(self):
        return pg_win_get_surface().get_flags()

    @flags.setter
    def flags(self, value: int):
        pg_win_set_mode(pg_win_get_size(), value, vsync=self._vsync)

    @property
    def vsync(self):
        return self._vsync

    @vsync.setter
    def vsync(self, value: bool):
        self._vsync = value
        pg_win_set_mode(pg_win_get_size(), pg_win_get_surface().get_flags(), vsync=value)

    @property
    def fullscreen(self):
        return bool(pg_win_get_surface().get_flags() & FULLSCREEN)

    @fullscreen.setter
    def fullscreen(self, value: bool):
        if not self.fullscreen and self.resizable:
            self._size = pg_win_get_size()

        new_size = pg_get_desktop_sizes()[0] if value and not self.fullscreen else self._size

        # ATTENTION: this segment is necessary because its absence will lead to such glitches as:
        # - froze of window content rendering
        # - graphical artifacts
        #
        # ALSO: this problem is detected for `pygame-ce==2.2.1`
        if self.fullscreen != value:
            self.vsync = False

        pg_win_set_mode(new_size, (self.flags | FULLSCREEN) if value else (self.flags & ~FULLSCREEN), vsync=self._vsync)

    @property
    def resizable(self):
        return bool(pg_win_get_surface().get_flags() & RESIZABLE)

    @resizable.setter
    def resizable(self, value: bool):
        self.flags = (self.flags | RESIZABLE) if value else (self.flags & ~RESIZABLE)

    @property
    def dt(self):
        return self._dt

    @property
    def is_running(self):
        return self._is_running

    def add_flags(self, flags: int):
        self.flags |= flags

    def remove_flags(self, flags: int):
        self.flags &= ~flags

    def get_buffered_events(self) -> tuple[Event]:
        return *self._event_buffer,

    def add_view(self, view):
        if view not in self._view_list:
            self._view_list.append(view)
            view._parent = self

    def remove_view(self, view):
        if view in self._view_list:
            self._view_list.remove(view)
            view._parent = None

    def has_view(self, view):
        return view in self._view_list

    def add_flippable(self, flippable: Flippable):
        if flippable not in self._flippable_list:
            self._flippable_list.append(flippable)

    def remove_flippable(self, flippable: Flippable):
        if flippable in self._flippable_list:
            self._flippable_list.remove(flippable)

    def has_flippable(self, flippable: Flippable):
        return flippable in self._flippable_list

    def add_renderable(self, renderable: Renderable):
        if renderable not in self._renderable_list:
            self._renderable_list.append(renderable)

    def remove_renderable(self, renderable: Renderable):
        if renderable in self._renderable_list:
            self._renderable_list.remove(renderable)

    def has_renderable(self, renderable: Renderable):
        return renderable in self._renderable_list

    def take_screenshot(self, save_directory='./screenshots', show_successful_toast=True):
        if not isdir(save_directory):
            makedirs(save_directory)

        file_name = 'screenshot_' + datetime.now().strftime("%d-%m-%Y-%H-%M-%S-%f") + '_'
        file_name += self.title.lower().replace(" ", "_") + '.png'

        pg_save_image(
            pg_win_get_surface(),
            save_directory + '/' + file_name
        )

        if show_successful_toast:
            self.show_toast(f'Screenshot "{file_name}" saved!')

    def show_toast(self, text, delay=Toast.SHORT_DELAY):
        return Toast(text, delay).show()

    def render_views(self):
        for view in self._view_list:
            view.render(pg_win_get_surface(), 0, 0, pg_win_get_size())

    def process_event(self, e: Event):
        if self.default_quit and e.type == QUIT:
            self.quit()
        elif e.type == WINDOWMOVED:
            self._pos = e.x, e.y

        if not self._is_running:  # ATTENTION: this check is needed to avoid crashes after calling `quit()`
            return

        for view in self._view_list:
            view.process_event(e, *pg_mouse_get_pos())

        get_mouse().process_event(e)
        get_input().process_event(e)

        if self.hold_event_buffer:
            self._event_buffer.append(e)

    def flip(self, read_events=True, render_views=False):
        current_time = time()

        self._event_buffer = []

        for flippable in self._flippable_list:
            flippable.flip()

        for view in self._view_list:
            # ATTENTION: the peculiarity is that the flip method is called before the render method is used
            view.flip()

        self.render_views()

        for renderable in self._renderable_list:
            renderable.render(pg_win_get_surface())

        render_toasts(pg_win_get_surface())

        pg_display_flip()
        get_mouse().flip()
        get_input().flip()

        self._fps_counter_num += 1

        if current_time - self._fps_counter_start_time >= 1:
            self._fps_counter_start_time = current_time
            self._fps_num = self._fps_counter_num
            self._fps_counter_num = 0

        if self.bg_color is not None:
            pg_win_get_surface().fill(self.bg_color)

        if self.fps_limit is None:
            self._dt = current_time - self._last_frame_time
        else:
            self._dt = self._clock.tick(self.fps_limit) / 1000

        if read_events:
            for e in get_events():
                self.process_event(e)

        self._last_frame_time = current_time

    def quit(self):
        self._is_running = False

        pg_quit()


__all__ = 'Window',
