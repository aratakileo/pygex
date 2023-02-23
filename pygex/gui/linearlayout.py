from pygex.gui.view import View, DEFAULT_PADDING, DEFAULT_SIZE, DEFAULT_POSITION, DEFAULT_GRAVITY
from pygex.color import TYPE_COLOR, COLOR_TRANSPARENT
from pygex.gui.drawable.drawable import Drawable
from pygame.event import Event
from typing import Sequence


class LinearLayout(View):
    def __init__(
            self,
            views: Sequence[View] = (),
            size: Sequence[int] = DEFAULT_SIZE,
            pos: Sequence[float | int] = DEFAULT_POSITION,
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity: int = DEFAULT_GRAVITY,
            background_drawable_or_color: Drawable | TYPE_COLOR = COLOR_TRANSPARENT,
            render_content_during_initialization: bool = True
    ):
        super().__init__(
            size,
            pos,
            padding,
            content_gravity,
            background_drawable_or_color,
            render_content_during_initialization
        )

        self._views = views

    def add_view(self, view: View):
        pass

    def remove_view(self, view: View):
        pass

    def process_event(self, e: Event):
        pass

    def flip(self):
        pass

    def render_content_surface(self):
        pass


__all__ = 'LinearLayout',
