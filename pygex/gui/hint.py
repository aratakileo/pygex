from pygex.color import TYPE_COLOR, as_rgba, to_readable_color, COLOR_BLACK
from pygex.text import render_text, DEFAULT_FONT_SIZE
from pygame.mouse import get_pos as pg_mouse_get_pos
from pygex.core import Renderable, get_window
from pygame.draw import rect as draw_rect
from pygame.surface import SurfaceType
from pygex.surface import AlphaSurface
from pygame.rect import RectType
from pygame.font import FontType
from typing import Sequence

GRAVITY_LEFT = GRAVITY_TOP = 0
GRAVITY_RIGHT = 1 << 0
GRAVITY_BOTTOM = 1 << 1
GRAVITY_CENTER_HORIZONTAL = 1 << 2
GRAVITY_CENTER_VERTICAL = 1 << 3
GRAVITY_LEFT_OF_CENTER = 1 << 4
GRAVITY_OVER_CENTER = 1 << 5
GRAVITY_RIGHT_OF_CENTER = 1 << 6
GRAVITY_UNDER_CENTER = 1 << 7


class Hint(Renderable):
    def __init__(
            self,
            text: str = ...,
            text_color: TYPE_COLOR = ...,
            bg_color: TYPE_COLOR = COLOR_BLACK | 0xaa000000,
            gravity=GRAVITY_CENTER_HORIZONTAL | GRAVITY_UNDER_CENTER,
            position_offset: Sequence[float | int] = (0, 0),
            strict_fit_in_bounds=True
    ):
        self.text = 'This is hint' if text is ... else text
        self.text_color = text_color
        self.bg_color = bg_color
        self.gravity = gravity
        self.strict_fit_in_bounds = strict_fit_in_bounds

        self.padding = 3
        self.font_or_size: FontType | int = ...
        self.border_radius_or_radii: int | Sequence[int] = 5
        self.position_offset = position_offset

        self._is_showing = False
        self._showing_pos: tuple[float | int, float | int] | None = None
        self._text_surface_buffer: SurfaceType | None = None

        get_window().add_renderable(self)

    def show(self):
        self._is_showing = True

    def hide(self):
        self._is_showing = False

    def provide_show(
            self,
            anchor_rect_or_pos: Sequence[float | int] | RectType = ...,
            bounds_in: Sequence[float | int] | RectType = ...
    ):
        if anchor_rect_or_pos is ...:
            anchor_rect_or_pos = pg_mouse_get_pos()

        if len(anchor_rect_or_pos) == 2:
            anchor_rect_or_pos = *anchor_rect_or_pos, 0, 0

        if bounds_in is ...:
            bounds_in = get_window().surface.get_bounding_rect()

        self._text_surface_buffer = render_text(
            self.text,
            self.text_color if self.text_color is not ... else to_readable_color(self.bg_color),
            DEFAULT_FONT_SIZE if self.font_or_size is ... else self.font_or_size
        )

        textw, texth = self._text_surface_buffer.get_size()
        boxw, boxh = textw + self.padding * 2, texth + self.padding * 2

        box_x, box_y = anchor_rect_or_pos[:2]

        is_gravity_left_of_center = self.gravity & GRAVITY_LEFT_OF_CENTER
        is_gravity_right_of_center = self.gravity & GRAVITY_RIGHT_OF_CENTER

        is_gravity_over_center = self.gravity & GRAVITY_OVER_CENTER
        is_gravity_under_center = self.gravity & GRAVITY_UNDER_CENTER

        if self.gravity & GRAVITY_RIGHT:
            box_x += anchor_rect_or_pos[2] - textw - self.padding * 2
        elif self.gravity & GRAVITY_CENTER_HORIZONTAL:
            box_x += (anchor_rect_or_pos[2] - textw) / 2 - self.padding * 2
        elif is_gravity_left_of_center:
            box_x -= textw + self.padding * 2
        elif is_gravity_right_of_center:
            box_x += anchor_rect_or_pos[2]

        if is_gravity_right_of_center and box_x + boxw > bounds_in[0] + bounds_in[2]:
            box_x = anchor_rect_or_pos[0] - textw - self.padding * 2
        elif is_gravity_left_of_center and box_x <= 0:
            box_x = anchor_rect_or_pos[0] + anchor_rect_or_pos[2]

        if self.gravity & GRAVITY_BOTTOM:
            box_y += anchor_rect_or_pos[3] - texth - self.padding * 2
        elif self.gravity & GRAVITY_CENTER_VERTICAL:
            box_y += (anchor_rect_or_pos[3] - texth) / 2 - self.padding * 2
        elif is_gravity_over_center:
            box_y -= texth + self.padding * 2
        elif is_gravity_under_center:
            box_y += anchor_rect_or_pos[3]

        if is_gravity_under_center and box_y + boxh > bounds_in[1] + bounds_in[3]:
            box_y = anchor_rect_or_pos[1] - texth - self.padding * 2
        elif is_gravity_over_center and box_y <= 0:
            box_y = anchor_rect_or_pos[1] + anchor_rect_or_pos[3]

        if self.strict_fit_in_bounds:
            if box_x + boxw > bounds_in[0] + bounds_in[2]:
                box_x = bounds_in[0] + bounds_in[2] - boxw
            elif box_x < bounds_in[0]:
                box_x = bounds_in[0]

            if box_y + boxh > bounds_in[1] + bounds_in[3]:
                box_y = bounds_in[1] + bounds_in[3] - boxh
            elif box_y < bounds_in[1]:
                box_y = bounds_in[1]

        self._showing_pos = box_x + self.position_offset[0], box_y + self.position_offset[1]

    def render(self, surface: SurfaceType):
        if self._showing_pos is None or self._text_surface_buffer is None or not self._is_showing:
            return

        boxw = self._text_surface_buffer.get_width() + self.padding * 2
        boxh = self._text_surface_buffer.get_height() + self.padding * 2

        box_surface = AlphaSurface((boxw, boxh))

        border_radii = (self.border_radius_or_radii,) if isinstance(self.border_radius_or_radii, int) \
            else (-1, *self.border_radius_or_radii)

        draw_rect(box_surface, as_rgba(self.bg_color), (0, 0, boxw, boxh), 0, *border_radii)

        surface.blit(box_surface, self._showing_pos)
        surface.blit(
            self._text_surface_buffer,
            (self._showing_pos[0] + self.padding, self._showing_pos[1] + self.padding)
        )


__all__ = (
    'GRAVITY_LEFT',
    'GRAVITY_TOP',
    'GRAVITY_LEFT_OF_CENTER',
    'GRAVITY_BOTTOM',
    'GRAVITY_RIGHT',
    'GRAVITY_RIGHT_OF_CENTER',
    'GRAVITY_CENTER_HORIZONTAL',
    'GRAVITY_CENTER_VERTICAL',
    'GRAVITY_OVER_CENTER',
    'GRAVITY_UNDER_CENTER',
    'Hint'
)
