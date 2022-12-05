from pygame.draw import line as draw_line
from pygame.surface import SurfaceType
from pygex.color import colorValue
from pygame.rect import RectType
from typing import Sequence
from math import ceil


def grid(
        surface: SurfaceType,
        line_color: colorValue,
        scale_interval: float | int,
        bounds: Sequence[float | int] | RectType,
        offset: Sequence[float | int] = (0, 0),
        line_width: int = 1
):
    """
    Drawing the basic grid
    :param surface: Surface on which the grid will be drawn
    :param line_color: grid line color
    :param scale_interval: distance between grid lines
    :param bounds: grid bounds in which the grid will be drawn
    :param offset: offset of drawing inside grid bounds
    :param line_width: grid line width
    """
    for ix in range(1, ceil(bounds[2] / scale_interval + 1)):
        x = bounds[0] + ix * scale_interval - offset[0] % scale_interval

        if x > bounds[0] + bounds[2] or x < bounds[0]:
            continue

        draw_line(surface, line_color, (x, bounds[1]), (x, bounds[1] + bounds[3]), line_width)

    for iy in range(1, ceil(bounds[3] / scale_interval + 1)):
        y = bounds[1] + iy * scale_interval - offset[1] % scale_interval

        if y > bounds[1] + bounds[3] or y < bounds[1]:
            continue

        draw_line(surface, line_color, (bounds[0], y), (bounds[0] + bounds[2], y), line_width)


__all__ = 'grid',
