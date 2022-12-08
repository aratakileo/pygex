from pygex.gui.drawable import Drawable, ColorDrawable
from pygex.text import SIZE_WRAP_CONTENT
from pygame.surface import SurfaceType
from pygex.color import colorValue
from typing import Sequence


DEFAULT_PADDING = (8, 8, 8, 8)


class View:
    def __init__(
            self,
            size: Sequence[int],
            pos: Sequence[float | int],
            padding: Sequence[int],
            background_drawable_or_color: Drawable | colorValue
    ):
        self.x, self.y = pos

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
    def rendered_width(self):
        return 0 if self._background_surface_buffer is None else self._background_surface_buffer.get_width()

    @property
    def rendered_height(self):
        return 0 if self._background_surface_buffer is None else self._background_surface_buffer.get_height()

    @property
    def rendered_size(self):
        return self.rendered_width, self.rendered_height

    def set_bg_drawable(self, drawable_or_color: Drawable | colorValue):
        if isinstance(drawable_or_color, Drawable):
            self._background_drawable = drawable_or_color
        else:
            self._background_drawable = ColorDrawable(drawable_or_color)

        self.render_background_surface(force_render=True)

    def render_content_surface(self):
        raise RuntimeError('Method `View.render_content_surface()` is not initialized!')

    def render_background_surface(self, force_render=False):
        if self._content_surface_buffer is None or self._background_drawable is None:
            return

        background_size = self._content_surface_buffer.get_size()
        background_size = (
            background_size[0] + self.padding[0] + self.padding[2],
            background_size[1] + self.padding[1] + self.padding[3]
        )

        if not force_render and self._background_surface_buffer is not None \
                and self._content_surface_buffer.get_size() == background_size:
            return

        self._background_surface_buffer = self._background_drawable.render(background_size)

    def render(self, surface: SurfaceType):
        if self._content_surface_buffer is None:
            self.render_content_surface()

        if self._background_drawable is not None:
            if self._background_surface_buffer is None:
                self.render_background_surface()

            surface.blit(self._background_surface_buffer, self.pos)

        surface.blit(self._content_surface_buffer, (self.x + self.padding[0], self.y + self.padding[1]))


__all__ = 'DEFAULT_PADDING', 'SIZE_WRAP_CONTENT', 'View'
