from pygex.color import TYPE_COLOR, to_pygame_alpha_color, COLOR_BLACK
from pygex.image import AlphaSurface, gradient, round_corners
from pygame.draw import rect as pg_draw_rect
from pygame.surface import SurfaceType
from typing import Sequence


class Drawable:
    def __init__(self, border_radius_or_radii: int | Sequence[int], border_width: int, border_color: TYPE_COLOR):
        if isinstance(border_radius_or_radii, int):
            self.set_border_radius(border_radius_or_radii)
        else:
            self.radii = border_radius_or_radii

        self.border_width = border_width
        self.border_color = border_color

    @property
    def has_border_radii(self):
        return (
            self.border_top_left_radius,
            self.border_top_right_radius,
            self.border_bottom_left_radius,
            self.border_bottom_right_radius
        ) != (-1, -1, -1, -1)

    @property
    def radii(self):
        return (
            self.border_top_left_radius,
            self.border_top_right_radius,
            self.border_bottom_left_radius,
            self.border_bottom_right_radius
        )

    @radii.setter
    def radii(self, new_radii: Sequence[int]):
        (
            self.border_top_left_radius,
            self.border_top_right_radius,
            self.border_bottom_left_radius,
            self.border_bottom_right_radius
        ) = new_radii

    def set_border_radius(self, radius: int):
        self.border_top_left_radius = radius
        self.border_top_right_radius = radius
        self.border_bottom_left_radius = radius
        self.border_bottom_right_radius = radius

    def render(self, size: Sequence[int]) -> SurfaceType:
        raise RuntimeError('Function `Drawable.render()` is not initialized!')


class LayerDrawable(Drawable):
    def __init__(
            self,
            layers: Sequence[Drawable],
            border_radius_or_radii: int | Sequence[int] = -1,
            border_width: int = 0,
            border_color: TYPE_COLOR = COLOR_BLACK
    ):
        super().__init__(border_radius_or_radii, border_width, border_color)
        self.layers = layers

    def render(self, size: Sequence[int]) -> SurfaceType | None:
        if not self.layers:
            return

        output_surface = self.layers[0].render(size)

        for layer in self.layers[1:]:
            output_surface.blit(layer.render(size), (0, 0))

        if self.has_border_radii:
            output_surface = round_corners(
                output_surface,
                self.border_top_left_radius,
                self.border_top_right_radius,
                self.border_bottom_left_radius,
                self.border_bottom_right_radius
            )

        if self.border_width > 0:
            pg_draw_rect(
                output_surface,
                to_pygame_alpha_color(self.border_color),
                (0, 0, *size),
                self.border_width,
                -1,
                self.border_top_left_radius,
                self.border_top_right_radius,
                self.border_bottom_left_radius,
                self.border_bottom_right_radius
            )

        return output_surface


class ColorDrawable(Drawable):
    def __init__(
            self,
            color: TYPE_COLOR,
            border_radius_or_radii: int | Sequence[int] = -1,
            border_width: int = 0,
            border_color: TYPE_COLOR = COLOR_BLACK
    ):
        super().__init__(border_radius_or_radii, border_width, border_color)

        self.color = color

    def render(self, size: Sequence[int]) -> SurfaceType:
        output_surface = AlphaSurface(size)

        pg_draw_rect(
            output_surface,
            to_pygame_alpha_color(self.color),
            (0, 0, *size),
            0,
            -1,
            self.border_top_left_radius,
            self.border_top_right_radius,
            self.border_bottom_left_radius,
            self.border_bottom_right_radius
        )

        if self.border_width > 0:
            pg_draw_rect(
                output_surface,
                to_pygame_alpha_color(self.border_color),
                (0, 0, *size),
                self.border_width,
                -1,
                self.border_top_left_radius,
                self.border_top_right_radius,
                self.border_bottom_left_radius,
                self.border_bottom_right_radius
            )

        return output_surface


class GradientDrawable(Drawable):
    def __init__(
            self,
            colors: Sequence[TYPE_COLOR],
            is_vertical=False,
            border_radius_or_radii: int | Sequence[int] = -1,
            border_width: int = 0,
            border_color: TYPE_COLOR = COLOR_BLACK
    ):
        super().__init__(border_radius_or_radii, border_width, border_color)

        self.colors = colors
        self.is_vertical = is_vertical

    def render(self, size: Sequence[int]) -> SurfaceType:
        output_surface = gradient(size, self.colors, self.is_vertical)

        if self.has_border_radii:
            output_surface = round_corners(
                output_surface,
                self.border_top_left_radius,
                self.border_top_right_radius,
                self.border_bottom_left_radius,
                self.border_bottom_right_radius
            )

        if self.border_width > 0:
            pg_draw_rect(
                output_surface,
                to_pygame_alpha_color(self.border_color),
                (0, 0, *size),
                self.border_width,
                -1,
                self.border_top_left_radius,
                self.border_top_right_radius,
                self.border_bottom_left_radius,
                self.border_bottom_right_radius
            )

        return output_surface


__all__ = 'Drawable', 'ColorDrawable', 'GradientDrawable', 'LayerDrawable'
