from pygex.gui.view import View, DEFAULT_PADDING, DEFAULT_SIZE, DEFAULT_POSITION, DEFAULT_GRAVITY
from pygex.gui.drawable.drawable import Drawable
from pygex.color import COLOR_TYPE
from pygame.event import Event
from typing import Sequence


# TODO: describe a `copy()` function for `Drawable` and after may be describe a constant `DEFAULT_BACKGROUND_DRAWABLE`, and use it like default value for `background_drawable_or_color` like `DEFAULT_BACKGROUND_DRAWABLE.copy()`
class LinearLayout(View):
    def __init__(
            self,
            views: Sequence[View] = (),
            size: Sequence[int] = DEFAULT_SIZE,
            pos: Sequence[float | int] = DEFAULT_POSITION,
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity: int = DEFAULT_GRAVITY,
            background_drawable_or_color: Drawable | COLOR_TYPE = None,
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
