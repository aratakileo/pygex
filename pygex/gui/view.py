from pygex.gui.drawable.drawable import Drawable, ColorDrawable
from pygame.display import get_window_size as pg_win_get_size
from pygex.text import SIZE_WRAP_CONTENT
from pygame.surface import SurfaceType
from functools import cached_property
from pygex.color import COLOR_TYPE
from typing import Sequence


DEFAULT_PADDING = (8, 8, 8, 8)

GRAVITY_LEFT = GRAVITY_TOP = 0
GRAVITY_RIGHT = 1 << 0
GRAVITY_BOTTOM = 1 << 1
GRAVITY_CENTER_HORIZONTAL = 1 << 2
GRAVITY_CENTER_VERTICAL = 1 << 3

VISIBILITY_VISIBLE = 0
VISIBILITY_INVISIBLE = 1
VISIBILITY_GONE = 2

SIZE_MATCH_PARENT = -1


class View:
    def __init__(
            self,
            size: Sequence[int],
            pos: Sequence[float | int],
            padding: Sequence[int],
            content_gravity: int,
            background_drawable_or_color: Drawable | COLOR_TYPE,
            render_content_during_initialization: bool
    ):
        self.x, self.y = pos
        self.content_gravity = content_gravity
        self.visibility = VISIBILITY_VISIBLE

        self._width, self._height = size
        self._padding_left, self._padding_top, self._padding_right, self._padding_bottom = padding

        self._background_surface_buffer: SurfaceType | None = None
        self._content_surface_buffer: SurfaceType | None = None
        self._parent: View | None = None

        if background_drawable_or_color is ...:
            self._background_drawable = None
        elif isinstance(background_drawable_or_color, Drawable):
            self._background_drawable = background_drawable_or_color
        else:
            self._background_drawable = ColorDrawable(background_drawable_or_color)

        if render_content_during_initialization:
            self.render_content_surface()

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

    @cached_property
    def get_min_width(self):
        return 50

    @cached_property
    def get_min_height(self):
        return 50

    @property
    def padding_left(self) -> int:
        return self._padding_left

    @padding_left.setter
    def padding_left(self, new_value: int):
        old_value = self._padding_left
        self._padding_left = new_value

        if new_value != old_value:
            self.render_background_surface(force_render=True)

    @property
    def padding_top(self) -> int:
        return self._padding_top

    @padding_top.setter
    def padding_top(self, new_value: int):
        old_value = self._padding_top
        self._padding_top = new_value

        if new_value != old_value:
            self.render_background_surface(force_render=True)

    @property
    def padding_right(self) -> int:
        return self._padding_right

    @padding_right.setter
    def padding_right(self, new_value: int):
        old_value = self._padding_right
        self._padding_right = new_value

        if new_value != old_value:
            self.render_background_surface(force_render=True)

    @property
    def padding_bottom(self) -> int:
        return self._padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, new_value: int):
        old_value = self._padding_bottom
        self._padding_bottom = new_value

        if new_value != old_value:
            self.render_background_surface(force_render=True)

    @property
    def padding(self) -> tuple[int]:
        return self._padding_left, self._padding_top, self._padding_right, self._padding_bottom

    @padding.setter
    def padding(self, new_value: Sequence[int]):
        old_value = self._padding_left, self._padding_top, self._padding_right, self._padding_bottom
        self._padding_left, self._padding_top, self._padding_right, self._padding_bottom = new_value

        if new_value != old_value:
            self.render_background_surface(force_render=True)

    @property
    def padding_horizontal(self) -> int:
        return self._padding_left + self._padding_right

    @property
    def padding_vertical(self) -> int:
        return self._padding_top + self._padding_bottom

    def get_computed_background_width(self):
        if self._width == SIZE_MATCH_PARENT:
            if self._parent is None or not isinstance(self._parent, View):
                return pg_win_get_size()[0]

            if self._parent._width == SIZE_WRAP_CONTENT:
                # ATTENTION: if there is no such condition, there will be an infinite recursion
                return self.get_min_width

            return self._parent.get_computed_background_width() - self._parent.padding_horizontal

        if self._width == SIZE_WRAP_CONTENT:
            if self._content_surface_buffer is None:
                return self.get_min_width

            return self._content_surface_buffer.get_width() + self.padding_horizontal

        return self._width

    def get_computed_background_height(self):
        if self._height == SIZE_MATCH_PARENT:
            if self._parent is None or not isinstance(self._parent, View):
                return pg_win_get_size()[1]

            if self._parent._height == SIZE_WRAP_CONTENT:
                # ATTENTION: if there is no such condition, there will be an infinite recursion
                return self.get_min_height

            return self._parent.get_computed_background_height() - self._parent.padding_vertical

        if self._height == SIZE_WRAP_CONTENT:
            if self._content_surface_buffer is None:
                return self.get_min_height

            return self._content_surface_buffer.get_height() + self.padding_vertical

        return self._height

    def get_computed_background_size(self):
        return self.get_computed_background_width(), self.get_computed_background_height()

    def get_computed_content_width(self):
        return self._width if self._width == SIZE_WRAP_CONTENT else (
                self.get_computed_background_width() - self.padding_horizontal
        )

    def get_computed_content_height(self):
        return self._height if self._height == SIZE_WRAP_CONTENT else (
                self.get_computed_background_height() - self.padding_vertical
        )

    def get_computed_content_size(self):
        return self.get_computed_content_width(), self.get_computed_content_height()

    def set_background_drawable(self, drawable_or_color: Drawable | COLOR_TYPE):
        if isinstance(drawable_or_color, Drawable):
            self._background_drawable = drawable_or_color
        else:
            self._background_drawable = ColorDrawable(drawable_or_color)

        self.render_background_surface(force_render=True)

    def get_background_drawable(self) -> Drawable | None:
        return self._background_drawable

    def render_content_surface(self):
        raise RuntimeError('Method `View.render_content_surface()` is not initialized!')

    def render_background_surface(self, force_render=False):
        if self._background_drawable is None or not force_render and self._background_surface_buffer is not None \
                and self._background_surface_buffer.get_size() == self.get_computed_background_size():
            return

        self._background_surface_buffer = self._background_drawable.render(self.get_computed_background_size())

    def render(self, surface: SurfaceType):
        if self.visibility != VISIBILITY_VISIBLE:
            return

        if self._content_surface_buffer is None:
            self.render_content_surface()

        if self._background_drawable is not None:
            if self._background_surface_buffer is None:
                self.render_background_surface()

            surface.blit(self._background_surface_buffer, self.pos)

        bg_width, bg_height = self.get_computed_background_width(), self.get_computed_background_height()

        if self._width == SIZE_MATCH_PARENT and self._background_surface_buffer.get_width() != bg_width \
                or self._height == SIZE_MATCH_PARENT and self._background_surface_buffer.get_height() != bg_height:
            self.render_content_surface()
            self.render_background_surface()

        content_x, content_y = self._padding_left, self._padding_top

        if self._content_surface_buffer is None:
            return

        content_width, content_height = self._content_surface_buffer.get_size()

        if self.content_gravity & GRAVITY_RIGHT:
            content_x = bg_width - content_width - self._padding_right
        elif self.content_gravity & GRAVITY_CENTER_HORIZONTAL:
            content_x = (bg_width - self.padding_horizontal - content_width) / 2 + self._padding_left

        if self.content_gravity & GRAVITY_BOTTOM:
            content_y = bg_height - content_height - self._padding_bottom
        elif self.content_gravity & GRAVITY_CENTER_VERTICAL:
            content_y = (bg_height - self.padding_vertical - content_height) / 2 + self._padding_top

        surface.blit(self._content_surface_buffer, (self.x + content_x, self.y + content_y))


__all__ = (
    'DEFAULT_PADDING',
    'GRAVITY_LEFT',
    'GRAVITY_TOP',
    'GRAVITY_RIGHT',
    'GRAVITY_BOTTOM',
    'GRAVITY_CENTER_HORIZONTAL',
    'GRAVITY_CENTER_VERTICAL',
    'VISIBILITY_VISIBLE',
    'VISIBILITY_INVISIBLE',
    'VISIBILITY_GONE',
    'SIZE_WRAP_CONTENT',
    'SIZE_MATCH_PARENT',
    'View'
)
