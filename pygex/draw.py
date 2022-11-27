from pygame.draw import line as draw_line, rect as draw_rect
from pygame.surface import SurfaceType
from pygex.color import colorValue
from pygex.text import render_text
from pygame.rect import RectType
from typing import Sequence
from math import ceil


def grid(
        surface: SurfaceType,
        color: colorValue,
        scale_interval: float | int,
        bounds: Sequence | RectType,
        offset: Sequence = (0, 0),
        width: int = 1
):
    for ix in range(1, ceil(bounds[2] / scale_interval + 1)):
        x = bounds[0] + ix * (scale_interval - width / 2) - offset[0] % (scale_interval - width / 2)

        if x > bounds[0] + bounds[2] or x < bounds[0]:
            continue

        draw_line(surface, color, (x, bounds[1]), (x, bounds[1] + bounds[3]), width)

    for iy in range(1, ceil(bounds[3] / scale_interval + 1)):
        y = bounds[1] + iy * (scale_interval - width / 2) - offset[1] % (scale_interval - width / 2)

        if y > bounds[1] + bounds[3] or y < bounds[1]:
            continue

        draw_line(surface, color, (bounds[0], y), (bounds[0] + bounds[2], y), width)


def hint(
        surface: SurfaceType,
        text,
        anchor_bounds: Sequence | RectType,
        bounds_in: Sequence,
        padding=3,
        upper=False,
        strict_fit_in=False
):
    text_surface = render_text(text, 0xffffff)
    textw, texth = text_surface.get_size()

    box_x = anchor_bounds[0] + (anchor_bounds[2] - textw) / 2 - padding * 2
    box_y = anchor_bounds[1] + anchor_bounds[3]
    boxw, boxh = textw + padding * 2, texth + padding * 2

    if box_y + boxh > bounds_in[1] + bounds_in[3] or (upper and anchor_bounds[1] > boxh):
        box_y = anchor_bounds[1] - texth - padding * 2

    if strict_fit_in:
        if box_x + boxw > bounds_in[0] + bounds_in[2]:
            box_x = bounds_in[0] + bounds_in[2] - boxw
        elif box_x < bounds_in[0]:
            box_x = bounds_in[0]

        if box_y + boxh > bounds_in[1] + bounds_in[3]:
            box_y = bounds_in[1] + bounds_in[3] - boxh
        elif box_y < bounds_in[1]:
            box_y = bounds_in[1]

    draw_rect(surface, 0, (box_x, box_y, boxw, boxh), 0, 5)

    surface.blit(text_surface, (box_x + padding, box_y + padding))
