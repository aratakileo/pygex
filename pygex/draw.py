from pygame.draw import line as pg_draw_line, rect as pg_draw_rect, ellipse as pg_draw_ellipse
from pygex.color import TYPE_COLOR, COLOR_TRANSPARENT, as_rgba
from pygex.surface import AlphaSurface, TYPE_SURFACE
from pygex.core.constants import MAX_BORDER_RADIUS
from pygame.rect import Rect as pg_Rect
from typing import Sequence
from math import ceil


def grid(
        surface: TYPE_SURFACE,
        line_color: TYPE_COLOR,
        scale_interval: float | int,
        bounds: Sequence[float | int] | pg_Rect,
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

        pg_draw_line(surface, line_color, (x, bounds[1]), (x, bounds[1] + bounds[3]), line_width)

    for iy in range(1, ceil(bounds[3] / scale_interval + 1)):
        y = bounds[1] + iy * scale_interval - offset[1] % scale_interval

        if y > bounds[1] + bounds[3] or y < bounds[1]:
            continue

        pg_draw_line(surface, line_color, (bounds[0], y), (bounds[0] + bounds[2], y), line_width)


def rect(
        surface: TYPE_SURFACE,
        color: TYPE_COLOR,
        _rect: Sequence[float | int] | pg_Rect,
        border_color: TYPE_COLOR = COLOR_TRANSPARENT,
        border_width: int = 0,
        border_radii: Sequence[int] = (0, 0, 0, 0),
        apply_alpha_color_over_surface=True
):
    """
    This method has an advantage over a similar method from pygame such as:

    - allows to set the border color independently of the main color
    - allows to draw the border together with the main part
    - with a radius value of -1 for any of the corners, draws all corners rounded as far as possible
    """
    draw_like_ellipse = MAX_BORDER_RADIUS in border_radii

    if apply_alpha_color_over_surface:
        surface_for_render = AlphaSurface(_rect[2:])
        rect_for_render = (0, 0, *_rect[2:])
    else:
        surface_for_render = surface
        rect_for_render = _rect

    if color != COLOR_TRANSPARENT:
        color = as_rgba(color)

        if draw_like_ellipse:
            pg_draw_ellipse(surface_for_render, color, rect_for_render)
        else:
            pg_draw_rect(surface_for_render, color, rect_for_render, 0, -1, *border_radii)

    if border_color != COLOR_TRANSPARENT and border_width > 0:
        border_color = as_rgba(border_color)

        if draw_like_ellipse:
            pg_draw_ellipse(surface_for_render, border_color, rect_for_render, border_width)
        else:
            pg_draw_rect(surface_for_render, border_color, rect_for_render, border_width, -1, *border_radii)

    if apply_alpha_color_over_surface:
        surface.blit(surface_for_render, _rect[:2])


__all__ = 'grid', 'rect'
