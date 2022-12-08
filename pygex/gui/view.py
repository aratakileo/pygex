from pygex.gui.drawable import Drawable, ColorDrawable
from pygex.text import SIZE_WRAP_CONTENT
from pygame.surface import SurfaceType
from pygex.color import colorValue
from typing import Sequence


DEFAULT_PADDING = (8, 8, 8, 8)

GRAVITY_LEFT = GRAVITY_TOP = 0
GRAVITY_RIGHT = 1 << 0
GRAVITY_BOTTOM = 1 << 1
GRAVITY_CENTER_HORIZONTAL = 1 << 2
GRAVITY_CENTER_VERTICAL = 1 << 3


class View:
    def __init__(
            self,
            size: Sequence[int],
            pos: Sequence[float | int],
            padding: Sequence[int],
            content_gravity: int,
            background_drawable_or_color: Drawable | colorValue
    ):
        self.x, self.y = pos
        self.content_gravity = content_gravity

        self._width, self._height = size
        self._padding = padding

        self._background_surface_buffer: SurfaceType | None = None
        self._content_surface_buffer: SurfaceType | None = None

        if background_drawable_or_color is ...:
            self._background_drawable = None
        elif isinstance(background_drawable_or_color, Drawable):
            self._background_drawable = background_drawable_or_color
        else:
            self._background_drawable = ColorDrawable(background_drawable_or_color)

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value: Sequence[float | int]):
        self.x, self.y = value

    @property
    def size(self):
        return self._width, self._height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        old_width = self._width

        self._width = value

        if value != old_width:
            self.render_content_surface()
            self.render_background_surface()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        old_height = self._height

        self._height = value

        if value != old_height:
            self.render_content_surface()
            self.render_background_surface()

    @size.setter
    def size(self, value: Sequence[int]):
        old_size = self._width, self._height

        self._width, self._height = value

        if value != old_size:
            self.render_content_surface()
            self.render_background_surface()

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, value: Sequence[int]):
        old_padding = self._padding

        self._padding = value

        if value != old_padding:
            self.render_background_surface()

    @property
    def _content_width(self):
        return self._width if self._width == SIZE_WRAP_CONTENT else (self._width - self._padding[0] - self._padding[2])

    @property
    def _content_height(self):
        return self._height if self._height == SIZE_WRAP_CONTENT \
            else (self._height - self._padding[1] - self._padding[3])

    @property
    def _content_size(self):
        return self._content_width, self._content_height

    @property
    def _background_width(self):
        return self._content_surface_buffer.get_width() + self._padding[0] + self._padding[2]

    @property
    def _background_height(self):
        return self._content_surface_buffer.get_height() + self._padding[1] + self._padding[3]

    @property
    def _background_size(self):
        return self._background_width, self._background_height

    def set_bg_drawable(self, drawable_or_color: Drawable | colorValue):
        if isinstance(drawable_or_color, Drawable):
            self._background_drawable = drawable_or_color
        else:
            self._background_drawable = ColorDrawable(drawable_or_color)

        self.render_background_surface(force_render=True)

    def render_content_surface(self):
        raise RuntimeError('Method `View.render_content_surface()` is not initialized!')

    def render_background_surface(self, force_render=False):
        if self._background_drawable is None or not force_render and self._background_surface_buffer is not None \
                and self._background_surface_buffer.get_size() == self._background_size:
            return

        self._background_surface_buffer = self._background_drawable.render(self._background_size)

    def render(self, surface: SurfaceType):
        if self._content_surface_buffer is None:
            self.render_content_surface()

        if self._background_drawable is not None:
            if self._background_surface_buffer is None:
                self.render_background_surface()

            surface.blit(self._background_surface_buffer, self.pos)

        surface.blit(self._content_surface_buffer, (self.x + self.padding[0], self.y + self.padding[1]))


__all__ = (
    'DEFAULT_PADDING',
    'GRAVITY_LEFT',
    'GRAVITY_TOP',
    'GRAVITY_RIGHT',
    'GRAVITY_BOTTOM',
    'GRAVITY_CENTER_HORIZONTAL',
    'GRAVITY_CENTER_VERTICAL',
    'SIZE_WRAP_CONTENT',
    'View'
)
