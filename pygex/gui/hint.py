from pygex.color import colorValue, to_pygame_alpha_color, get_readable_text_color
from pygame.draw import rect as draw_rect
from pygame.surface import SurfaceType
from pygex.image import AlphaSurface
from pygex.text import render_text
from pygame.rect import RectType
from pygame.font import FontType
from typing import Sequence


class Hint:
    GRAVITY_LEFT = GRAVITY_TOP = 0
    GRAVITY_RIGHT = 1 << 0
    GRAVITY_BOTTOM = 1 << 1
    GRAVITY_CENTER_HORIZONTAL = 1 << 2
    GRAVITY_CENTER_VERTICAL = 1 << 3
    GRAVITY_LEFT_OF_CENTER = 1 << 4
    GRAVITY_OVER_CENTER = 1 << 5
    GRAVITY_RIGHT_OF_CENTER = 1 << 6
    GRAVITY_UNDER_CENTER = 1 << 7

    def __init__(
            self,
            text,
            text_color: colorValue = ...,
            bg_color: colorValue = 0xaa000000,
            gravity=GRAVITY_CENTER_HORIZONTAL | GRAVITY_UNDER_CENTER,
            strict_fit_in_bounds=True
    ):
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.gravity = gravity
        self.strict_fit_in_bounds = strict_fit_in_bounds

        self.padding = 3
        self.font_or_size: FontType | int = ...
        self.border_radius_or_radii: int | Sequence[int] = 5

    def render(
            self,
            surface: SurfaceType,
            anchor_rect_or_point: Sequence[float | int] | RectType,
            bounds_in: Sequence[float | int] | RectType
    ):
        if len(anchor_rect_or_point) == 2:
            anchor_rect_or_point = *anchor_rect_or_point, 0, 0

        text_color = self.text_color if self.text_color is not ... else get_readable_text_color(self.bg_color)

        if self.font_or_size is not ...:
            text_surface = render_text(self.text, text_color, self.font_or_size)
        else:
            text_surface = render_text(self.text, text_color)

        textw, texth = text_surface.get_size()
        boxw, boxh = textw + self.padding * 2, texth + self.padding * 2

        box_x, box_y = anchor_rect_or_point[:2]

        is_gravity_left_of_center = self.gravity & Hint.GRAVITY_LEFT_OF_CENTER
        is_gravity_right_of_center = self.gravity & Hint.GRAVITY_RIGHT_OF_CENTER

        is_gravity_over_center = self.gravity & Hint.GRAVITY_OVER_CENTER
        is_gravity_under_center = self.gravity & Hint.GRAVITY_UNDER_CENTER

        if self.gravity & Hint.GRAVITY_RIGHT:
            box_x += anchor_rect_or_point[2] - textw - self.padding * 2
        elif self.gravity & Hint.GRAVITY_CENTER_HORIZONTAL:
            box_x += (anchor_rect_or_point[2] - textw) / 2 - self.padding * 2
        elif is_gravity_left_of_center:
            box_x -= textw + self.padding * 2
        elif is_gravity_right_of_center:
            box_x += anchor_rect_or_point[2]

        if is_gravity_right_of_center and box_x + boxw > bounds_in[0] + bounds_in[2]:
            box_x = anchor_rect_or_point[0] - textw - self.padding * 2
        elif is_gravity_left_of_center and box_x <= 0:
            box_x = anchor_rect_or_point[0] + anchor_rect_or_point[2]

        if self.gravity & Hint.GRAVITY_BOTTOM:
            box_y += anchor_rect_or_point[3] - texth - self.padding * 2
        elif self.gravity & Hint.GRAVITY_CENTER_VERTICAL:
            box_y += (anchor_rect_or_point[3] - texth) / 2 - self.padding * 2
        elif is_gravity_over_center:
            box_y -= texth + self.padding * 2
        elif is_gravity_under_center:
            box_y += anchor_rect_or_point[3]

        if is_gravity_under_center and box_y + boxh > bounds_in[1] + bounds_in[3]:
            box_y = anchor_rect_or_point[1] - texth - self.padding * 2
        elif is_gravity_over_center and box_y <= 0:
            box_y = anchor_rect_or_point[1] + anchor_rect_or_point[3]

        if self.strict_fit_in_bounds:
            if box_x + boxw > bounds_in[0] + bounds_in[2]:
                box_x = bounds_in[0] + bounds_in[2] - boxw
            elif box_x < bounds_in[0]:
                box_x = bounds_in[0]

            if box_y + boxh > bounds_in[1] + bounds_in[3]:
                box_y = bounds_in[1] + bounds_in[3] - boxh
            elif box_y < bounds_in[1]:
                box_y = bounds_in[1]

        box_surface = AlphaSurface((boxw, boxh))

        border_radii = (self.border_radius_or_radii,) if isinstance(self.border_radius_or_radii, int) \
            else (-1, *self.border_radius_or_radii)

        draw_rect(box_surface, to_pygame_alpha_color(self.bg_color), (0, 0, boxw, boxh), 0, *border_radii)

        surface.blit(box_surface, (box_x, box_y))
        surface.blit(text_surface, (box_x + self.padding, box_y + self.padding))


__all__ = 'Hint',
