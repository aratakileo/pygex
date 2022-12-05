from pygame.draw import line as draw_line
from pygame.surface import SurfaceType
from pygex.color import colorValue
from pygame.rect import RectType
from typing import Sequence
from math import ceil


def grid(
        surface: SurfaceType,
        color: colorValue,
        scale_interval: float | int,
        bounds: Sequence[float | int] | RectType,
        offset: Sequence[float | int] = (0, 0),
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


__all__ = 'grid',
