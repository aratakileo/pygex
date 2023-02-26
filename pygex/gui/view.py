from pygex.gui.drawable.interactiondrawable import InteractionDrawable, INTERACTION_STATE_NO_INTERACTION
from pygame.constants import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, WINDOWLEAVE
from pygex.gui.drawable.interactiondrawable import INTERACTION_STATE_END_OF_INTERACTION
from pygex.gui.drawable.interactiondrawable import INTERACTION_STATE_IN_INTERACTION
from pygex.gui.drawable.drawable import Drawable, ColorDrawable
from pygame.display import get_window_size as pg_win_get_size
from pygex.color import TYPE_COLOR, COLOR_TRANSPARENT
from pygame.mouse import get_pos as pg_mouse_get_pos
from pygex.text import SIZE_WRAP_CONTENT
from pygame.surface import SurfaceType
from functools import cached_property
from pygex.gui.hint import Hint
from pygame.event import Event
from pygame.rect import Rect
from typing import Sequence


GRAVITY_LEFT = GRAVITY_TOP = 0
GRAVITY_RIGHT = 1 << 0
GRAVITY_BOTTOM = 1 << 1
GRAVITY_CENTER_HORIZONTAL = 1 << 2
GRAVITY_CENTER_VERTICAL = 1 << 3

VISIBILITY_VISIBLE = 0
VISIBILITY_INVISIBLE = 1
VISIBILITY_GONE = 2

SIZE_MATCH_PARENT = -1

DEFAULT_PADDING = (8, 8, 8, 8)
DEFAULT_SIZE = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT)
DEFAULT_POSITION = (0, 0)
DEFAULT_GRAVITY = GRAVITY_LEFT | GRAVITY_TOP


class View:
    def __init__(
            self,
            size: Sequence[int],
            pos: Sequence[float | int],
            padding: Sequence[int],
            content_gravity: int,
            background_drawable_or_color: Drawable | TYPE_COLOR,
            prerender_during_initialization: bool
    ):
        self._width, self._height = size
        self._padding_left, self._padding_top, self._padding_right, self._padding_bottom = padding

        self._background_drawable_is_interaction_drawable = False
        self._background_surface_buffer: SurfaceType | None = None
        self._parent: View | None = None

        if background_drawable_or_color is None or background_drawable_or_color == COLOR_TRANSPARENT:
            self._background_drawable = None
        elif isinstance(background_drawable_or_color, Drawable):
            self._background_drawable = background_drawable_or_color
            self._background_drawable_is_interaction_drawable = isinstance(
                self._background_drawable,
                InteractionDrawable
            )
        else:
            self._background_drawable = ColorDrawable(background_drawable_or_color)

        self._interaction_state = INTERACTION_STATE_NO_INTERACTION
        self._is_focused = False

        self._hint: Hint | None = None
        self._hint_offset = 3
        self._hint_anchor_is_mouse = False

        self.x, self.y = pos
        self.content_gravity = content_gravity
        self.visibility = VISIBILITY_VISIBLE
        self.enabled = True

        if prerender_during_initialization:
            self.render_content_surface()
            self.render_background_surface()

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

        if value == old_width:
            return

        self.render_content_surface()
        self.render_background_surface()

        if 'rebufferize_sizes_for_view' in self._parent.__dir__():
            self._parent.rebufferize_sizes_for_view(self)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        old_height = self._height

        self._height = value

        if value == old_height:
            return

        self.render_content_surface()
        self.render_background_surface()

        if 'rebufferize_sizes_for_view' in self._parent.__dir__():
            self._parent.rebufferize_sizes_for_view(self)

    @size.setter
    def size(self, value: Sequence[int]):
        old_size = self._width, self._height

        self._width, self._height = value

        if value == old_size:
            return

        self.render_content_surface()
        self.render_background_surface()

        if 'rebufferize_sizes_for_view' in self._parent.__dir__():
            self._parent.rebufferize_sizes_for_view(self)

    @cached_property
    def min_width(self):
        return 50

    @cached_property
    def min_height(self):
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

    @property
    def is_clicked(self):
        return self._interaction_state == INTERACTION_STATE_END_OF_INTERACTION

    @property
    def is_focused(self):
        return self._is_focused

    @property
    def buffered_content_surface(self) -> SurfaceType | None:
        return

    def get_bounds(self):
        return Rect(
            self.x,
            self.y,
            self.get_computed_background_width(),
            self.get_computed_background_height(),
        )

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

    def get_computed_background_width(self):
        if self._width == SIZE_MATCH_PARENT:
            if self._parent is None or not isinstance(self._parent, View):
                return pg_win_get_size()[0]

            if self._parent._width == SIZE_WRAP_CONTENT:
                # ATTENTION: if there is no such condition, there will be an infinite recursion
                return self.min_width

            return self._parent.get_computed_background_width() - self._parent.padding_horizontal

        if self._width == SIZE_WRAP_CONTENT:
            if self.buffered_content_surface is None:
                return self.min_width

            return self.buffered_content_surface.get_width() + self.padding_horizontal

        return self._width

    def get_computed_background_height(self):
        if self._height == SIZE_MATCH_PARENT:
            if self._parent is None or not isinstance(self._parent, View):
                return pg_win_get_size()[1]

            if self._parent._height == SIZE_WRAP_CONTENT:
                # ATTENTION: if there is no such condition, there will be an infinite recursion
                return self.min_height

            return self._parent.get_computed_background_height() - self._parent.padding_vertical

        if self._height == SIZE_WRAP_CONTENT:
            if self.buffered_content_surface is None:
                return self.min_height

            return self.buffered_content_surface.get_height() + self.padding_vertical

        return self._height

    def get_computed_background_size(self):
        return self.get_computed_background_width(), self.get_computed_background_height()

    def get_background_drawable(self) -> Drawable | None:
        return self._background_drawable

    def set_background_drawable(self, drawable_or_color: Drawable | TYPE_COLOR | None):
        if isinstance(drawable_or_color, Drawable):
            self._background_drawable = drawable_or_color
            self._background_drawable_is_interaction_drawable = isinstance(
                self._background_drawable,
                InteractionDrawable
            )
        elif drawable_or_color is None or drawable_or_color == COLOR_TRANSPARENT:
            self._background_drawable = None
            self._background_drawable_is_interaction_drawable = False
        else:
            self._background_drawable = ColorDrawable(drawable_or_color)
            self._background_drawable_is_interaction_drawable = False

        self.render_background_surface(force_render=True)

    def set_hint(
            self,
            text: str,
            offset=3,
            anchor_is_mouse=False,
            hint_gravity: int = Hint.GRAVITY_CENTER_HORIZONTAL | Hint.GRAVITY_UNDER_CENTER
    ):
        self._hint_offset = offset
        self._hint_anchor_is_mouse = anchor_is_mouse

        if self._hint is None:
            self._hint = Hint(text, gravity=hint_gravity)

            return

        self._hint.text = text
        self._hint.gravity = hint_gravity

    def process_event(self, e: Event, offsetted_mouse_x: int, offsetted_mouse_y: int) -> bool:
        if self.visibility == VISIBILITY_GONE or not self.enabled:
            return True

        if e.type == WINDOWLEAVE:
            # ATTENTION: This is necessary so that the focus is removed from the View when the mouse goes outside
            # the window, while the View is at the window border, which is why the mouse coordinates are not updated
            # and the events associated with it are no longer read
            self._is_focused = False

        interaction_status_is_changed = False

        if e.type == MOUSEMOTION:
            self._is_focused = self.get_bounds().collidepoint(offsetted_mouse_x, offsetted_mouse_y)
            return not self._is_focused and self._interaction_state == INTERACTION_STATE_NO_INTERACTION

        if e.type == MOUSEBUTTONDOWN and self._is_focused:
            self._interaction_state = INTERACTION_STATE_IN_INTERACTION
            interaction_status_is_changed = True
        elif e.type == MOUSEBUTTONUP and self._interaction_state == INTERACTION_STATE_IN_INTERACTION:
            self._interaction_state = INTERACTION_STATE_END_OF_INTERACTION if self._is_focused \
                else INTERACTION_STATE_NO_INTERACTION
            interaction_status_is_changed = True

        if interaction_status_is_changed:
            if self._background_drawable_is_interaction_drawable:
                self._background_drawable.set_interaction_state(self._interaction_state)

                if self._interaction_state == INTERACTION_STATE_IN_INTERACTION:
                    self._background_surface_buffer = self._background_drawable.render(
                        self.get_computed_background_size()
                    )

                    if isinstance(self._parent, View):
                        self._parent.render_content_surface()

            return False

        return True

    def flip(self):
        # ATTENTION: if the View like a ButtonView will be added to the Window view list,
        # then this method will call earlier than the render method

        if self.visibility == VISIBILITY_GONE or not self.enabled:
            self._interaction_state = INTERACTION_STATE_NO_INTERACTION
            self._is_focused = False

            if self._background_drawable_is_interaction_drawable \
                    and self._background_drawable._interaction_state != INTERACTION_STATE_NO_INTERACTION:

                self._background_drawable.set_interaction_state(INTERACTION_STATE_NO_INTERACTION, animate=False)
                self._background_surface_buffer = self._background_drawable.render(self.get_computed_background_size())

                if isinstance(self._parent, View):
                    self._parent.render_content_surface()

            return

        if self._interaction_state == INTERACTION_STATE_END_OF_INTERACTION:
            self._interaction_state = INTERACTION_STATE_NO_INTERACTION

            if self._background_drawable_is_interaction_drawable:
                self._background_drawable.set_interaction_state(self._interaction_state)

        if self._background_drawable_is_interaction_drawable:
            self._background_drawable.flip()

    def render_content_surface(self):
        pass

    def render_background_surface(self, force_render=False):
        if self._background_drawable is None or not force_render and self._background_surface_buffer is not None \
                and self._background_surface_buffer.get_size() == self.get_computed_background_size():
            return

        self._background_surface_buffer = self._background_drawable.render(self.get_computed_background_size())

        if isinstance(self._parent, View):
            self._parent.render_content_surface()

    def render(self, surface: SurfaceType, x_off: float | int, y_off: float | int, parent_size: Sequence[int]):
        if self.visibility != VISIBILITY_VISIBLE:
            return

        render_x, render_y = self.x + x_off, self.y + y_off

        if self._background_drawable_is_interaction_drawable and self._background_drawable.is_need_to_be_rendered:
            self._background_surface_buffer = self._background_drawable.render(self.get_computed_background_size())

        if self.buffered_content_surface is None:
            self.render_content_surface()

        if self._background_drawable is not None:
            if self._background_surface_buffer is None:
                self.render_background_surface()

            surface.blit(self._background_surface_buffer, (render_x, render_y))

        bg_width, bg_height = self.get_computed_background_width(), self.get_computed_background_height()

        if self._width == SIZE_MATCH_PARENT and self._background_surface_buffer.get_width() != bg_width \
                or self._height == SIZE_MATCH_PARENT and self._background_surface_buffer.get_height() != bg_height:
            self.render_content_surface()
            self.render_background_surface()

        if self.buffered_content_surface is not None:
            content_x, content_y = self._padding_left, self._padding_top
            content_width, content_height = self.buffered_content_surface.get_size()

            if self.content_gravity & GRAVITY_RIGHT:
                content_x = bg_width - content_width - self._padding_right
            elif self.content_gravity & GRAVITY_CENTER_HORIZONTAL:
                content_x = (bg_width - self.padding_horizontal - content_width) / 2 + self._padding_left

            if self.content_gravity & GRAVITY_BOTTOM:
                content_y = bg_height - content_height - self._padding_bottom
            elif self.content_gravity & GRAVITY_CENTER_VERTICAL:
                content_y = (bg_height - self.padding_vertical - content_height) / 2 + self._padding_top

            surface.blit(self.buffered_content_surface, (render_x + content_x, render_y + content_y))

        if self._is_focused and self._hint is not None:
            hint_pos = pg_mouse_get_pos() if self._hint_anchor_is_mouse else (
                render_x + (self.get_computed_background_width() / 2),
                render_y + self.get_computed_background_height() + self._hint_offset
            )

            self._hint.render(
                surface,
                hint_pos,
                (0, 0, *parent_size)
            )


__all__ = (
    'DEFAULT_PADDING',
    'DEFAULT_SIZE',
    'DEFAULT_POSITION',
    'DEFAULT_GRAVITY',
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
