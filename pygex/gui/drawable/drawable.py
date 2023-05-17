from pygex.color import TYPE_COLOR, COLOR_TRANSPARENT
from pygex.surface import AlphaSurface, TYPE_SURFACE
from pygex.transform import gradient, round_corners
from pygex.draw import rect as draw_rect
from typing import Sequence


class Drawable:
    def __init__(self, border_radius_or_radii: int | Sequence[int], border_width: int, border_color: TYPE_COLOR):
        if isinstance(border_radius_or_radii, int):
            self.set_border_radius(border_radius_or_radii)
        else:
            self.border_radii = border_radius_or_radii

        self.border_width = border_width
        self.border_color = border_color

    @property
    def has_border_radii(self):
        return (
            self.border_top_left_radius,
            self.border_top_right_radius,
            self.border_bottom_left_radius,
            self.border_bottom_right_radius
        ) != (0, 0, 0, 0)

    @property
    def border_radii(self) -> tuple[int, int, int, int]:
        return (
            self.border_top_left_radius,
            self.border_top_right_radius,
            self.border_bottom_left_radius,
            self.border_bottom_right_radius
        )

    @border_radii.setter
    def border_radii(self, new_radii: Sequence[int]):
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

    def render(self, size: Sequence[int]) -> TYPE_SURFACE:
        raise RuntimeError('Function `Drawable.render()` is not initialized!')


class LayerDrawable(Drawable):
    def __init__(
            self,
            layers: Sequence[Drawable],
            border_radius_or_radii: int | Sequence[int] = 0,
            border_width: int = 0,
            border_color: TYPE_COLOR = COLOR_TRANSPARENT
    ):
        super().__init__(border_radius_or_radii, border_width, border_color)
        self.layers = layers

    def render(self, size: Sequence[int]) -> TYPE_SURFACE | None:
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

        draw_rect(
            output_surface,
            COLOR_TRANSPARENT,
            (0, 0, *size),
            self.border_color,
            self.border_width,
            self.border_radii,
        )

        return output_surface


class ColorDrawable(Drawable):
    def __init__(
            self,
            color: TYPE_COLOR,
            border_radius_or_radii: int | Sequence[int] = 0,
            border_width: int = 0,
            border_color: TYPE_COLOR = COLOR_TRANSPARENT
    ):
        super().__init__(border_radius_or_radii, border_width, border_color)

        self.color = color

    def render(self, size: Sequence[int]) -> TYPE_SURFACE:
        output_surface = AlphaSurface(size)

        draw_rect(
            output_surface,
            self.color,
            (0, 0, *size),
            self.border_color,
            self.border_width,
            self.border_radii,

            # ATTENTION: drawing rect already happens on a clean Surface, so this functionality is not needed
            apply_alpha_color_over_surface=False
        )

        return output_surface


class GradientDrawable(Drawable):
    def __init__(
            self,
            colors: Sequence[TYPE_COLOR],
            is_vertical=False,
            border_radius_or_radii: int | Sequence[int] = 0,
            border_width: int = 0,
            border_color: TYPE_COLOR = COLOR_TRANSPARENT
    ):
        super().__init__(border_radius_or_radii, border_width, border_color)

        self.colors = colors
        self.is_vertical = is_vertical

    def render(self, size: Sequence[int]) -> TYPE_SURFACE:
        output_surface = gradient(size, self.colors, self.is_vertical)

        if self.has_border_radii:
            output_surface = round_corners(
                output_surface,
                self.border_top_left_radius,
                self.border_top_right_radius,
                self.border_bottom_left_radius,
                self.border_bottom_right_radius
            )

        draw_rect(
            output_surface,
            COLOR_TRANSPARENT,
            (0, 0, *size),
            self.border_color,
            self.border_width,
            self.border_radii,
        )

        return output_surface


__all__ = 'Drawable', 'ColorDrawable', 'GradientDrawable', 'LayerDrawable'
