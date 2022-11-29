from pygex.color import colorValue, to_pygame_alpha_color
from pygame.draw import rect as draw_rect
from pygame.surface import SurfaceType
from pygex.image import AlphaSurface
from pygex.text import render_text
from pygame.rect import RectType
from pygame.font import FontType
from typing import Sequence


class Hint:
    def __init__(
            self,
            text,
            text_color: colorValue = 0xffffff,
            bg_color: colorValue = 0xaa000000,
            is_upper=False,
            strict_fit_in_bounds=True
    ):
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.is_upper = is_upper
        self.strict_fit_in_bounds = strict_fit_in_bounds

        self.padding = 3
        self.font_or_size: FontType | int = ...

    def render(self, surface: SurfaceType, anchor_bounds: Sequence | RectType, bounds_in: Sequence | RectType,):
        if self.font_or_size is not ...:
            text_surface = render_text(self.text, self.text_color, self.font_or_size)
        else:
            text_surface = render_text(self.text, self.text_color)

        textw, texth = text_surface.get_size()

        box_x = anchor_bounds[0] + (anchor_bounds[2] - textw) / 2 - self.padding * 2
        box_y = anchor_bounds[1] + anchor_bounds[3]
        boxw, boxh = textw + self.padding * 2, texth + self.padding * 2

        if box_y + boxh > bounds_in[1] + bounds_in[3] or (self.is_upper and anchor_bounds[1] > boxh):
            box_y = anchor_bounds[1] - texth - self.padding * 2

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

        draw_rect(box_surface, to_pygame_alpha_color(self.bg_color), (0, 0, boxw, boxh), 0, 5)

        surface.blit(box_surface, (box_x, box_y))
        surface.blit(text_surface, (box_x + self.padding, box_y + self.padding))


__all__ = 'Hint',
