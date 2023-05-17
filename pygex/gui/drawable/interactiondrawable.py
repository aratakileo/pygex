from pygex.color import TYPE_COLOR, COLOR_TRANSPARENT, COLOR_WHITE, ahex_to_rgba, as_ahex, as_rgba, to_readable_color
from pygex.gui.drawable.drawable import Drawable, ColorDrawable
from pygex.surface import AlphaSurface, TYPE_SURFACE
from pygex.core.interface import Flippable
from pygex.transform import round_corners
from pygex.draw import rect as draw_rect
from pygex.color import replace_alpha
from typing import Sequence


INTERACTION_STATE_NO_INTERACTION = 0
INTERACTION_STATE_IN_INTERACTION = 1
INTERACTION_STATE_END_OF_INTERACTION = 2


class InteractionDrawable(Drawable, Flippable):
    def __init__(
            self,
            content: Drawable,
            border_radius_or_radii: int | Sequence[int] = ...,
            border_width: int = 0,
            border_color: TYPE_COLOR = COLOR_TRANSPARENT
    ):
        if border_radius_or_radii is ...:
            if content is None:
                border_radius_or_radii = 0
            else:
                border_radius_or_radii = content.border_radii

        super().__init__(border_radius_or_radii, border_width, border_color)

        self._is_in_process = False
        self._interaction_state = INTERACTION_STATE_NO_INTERACTION

        self._content_drawable = content
        self._content_buffered_size = (-1, -1)
        self._content_buffered_surface: TYPE_SURFACE | None = None

    @staticmethod
    def from_color_content(
            color: TYPE_COLOR,
            border_radius_or_radii: int | Sequence[int] = 0
    ):
        if color == COLOR_TRANSPARENT:
            return

        return InteractionDrawable(ColorDrawable(color, border_radius_or_radii))

    @property
    def is_need_to_be_rendered(self):
        return self._is_in_process

    def get_content_drawable(self):
        return self._content_drawable

    def set_content_drawable(self, content: Drawable):
        self._content_drawable = content
        self._content_buffered_size = (-1, -1)

    def set_interaction_state(self, interaction_status: int, animate=True):
        if (
                interaction_status == INTERACTION_STATE_NO_INTERACTION
                and self._interaction_state != INTERACTION_STATE_NO_INTERACTION
                and animate
        ):
            self._is_in_process = True

        self._interaction_state = interaction_status


class FadingDrawable(InteractionDrawable):
    def __init__(
            self,
            content: Drawable = None,
            effect_color: TYPE_COLOR = COLOR_WHITE | 0x96000000,
            border_radius_or_radii: int | Sequence[int] = ...,
            border_width: int = 0,
            border_color: TYPE_COLOR = COLOR_TRANSPARENT
    ):
        super().__init__(content, border_radius_or_radii, border_width, border_color)

        self._effect_color = effect_color
        self._effect_color_rgba = ahex_to_rgba(as_ahex(effect_color))
        self._in_process_alpha_of_background = self._effect_color_rgba[-1]
        self._in_process_alpha_of_border = self._effect_color_rgba[-1]

        self.effect_border_width = 2
        self.effect_alpha_value_difference_for_start_decreasing_effect_border_alpha_value = 80
        self.effect_alpha_decreasing_per_frame = 3

    @staticmethod
    def from_color_content(
            color: TYPE_COLOR,
            border_radius_or_radii: int | Sequence[int] = 0,
            effect_color: TYPE_COLOR = ...,
            effect_alpha: int = ...
    ):
        if color == COLOR_TRANSPARENT:
            return

        if effect_color is ...:
            if effect_alpha is ...:
                effect_alpha = 0x96

            effect_color = replace_alpha(to_readable_color(color), effect_alpha)
        elif effect_alpha is not ...:
            effect_color = replace_alpha(as_ahex(effect_color), effect_alpha)

        return FadingDrawable(ColorDrawable(color, border_radius_or_radii), effect_color)

    @property
    def effect_color(self):
        return self._effect_color

    @effect_color.setter
    def effect_color(self, new_effect_color: TYPE_COLOR):
        self._effect_color = new_effect_color
        self._effect_color_rgba = ahex_to_rgba(as_ahex(new_effect_color))

    def set_interaction_state(self, interaction_state: int, animate=True):
        if (
                interaction_state == INTERACTION_STATE_NO_INTERACTION
                and self._interaction_state != INTERACTION_STATE_NO_INTERACTION
                and animate
        ):
            self._is_in_process = True

        self._interaction_state = interaction_state
        self._in_process_alpha_of_background = self._effect_color_rgba[-1]
        self._in_process_alpha_of_border = self._effect_color_rgba[-1]

    def flip(self):
        """This method should be called every `flip()` call of custom View"""
        if self._is_in_process:
            if self._in_process_alpha_of_background > 0:
                self._in_process_alpha_of_background -= self.effect_alpha_decreasing_per_frame

            if self._in_process_alpha_of_background <= (
                    self._effect_color_rgba[-1]
                    - self.effect_alpha_value_difference_for_start_decreasing_effect_border_alpha_value
            ):
                self._in_process_alpha_of_border -= self.effect_alpha_decreasing_per_frame

        if self._in_process_alpha_of_border <= 0:
            self._is_in_process = False

    def render(self, size: Sequence[int]) -> TYPE_SURFACE | None:
        # STEP 1: rendering or getting content from buffer for the output surface
        if size != self._content_buffered_size:
            self._content_buffered_size = size
            self._content_buffered_surface = self._content_drawable.render(size)

        output_surface = self._content_buffered_surface.copy()

        # STEP 2: rendering effect on the output surface
        if self._interaction_state == INTERACTION_STATE_IN_INTERACTION:
            effect_surface = AlphaSurface(size)
            effect_surface.fill(as_rgba(self._effect_color))
            output_surface.blit(effect_surface, (0, 0))
        elif self._is_in_process:
            effect_surface = AlphaSurface(size)

            if self._in_process_alpha_of_background > 0:
                # ATTENTION: In this case, the method of simply filling in the Surface is used, and not drawing
                # a rounded rect, since the output Surface will be rounded later anyway
                effect_surface.fill((*self._effect_color_rgba[:3], self._in_process_alpha_of_background))

            draw_rect(
                effect_surface,
                COLOR_TRANSPARENT,
                (0, 0, *size),
                (*self._effect_color_rgba[:3], self._in_process_alpha_of_border),
                self.effect_border_width,
                self.border_radii,

                # ATTENTION: in this case, there is no need to impose this border on the filled surface, here it
                # is necessary that the border color replace the color on the filled surface, for the correct rendering
                # of the animation
                apply_alpha_color_over_surface=False
            )

            output_surface.blit(effect_surface, (0, 0))

        # STEP 3: rounding and bordering the output surface
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


__all__ = (
    'InteractionDrawable',
    'FadingDrawable',
    'INTERACTION_STATE_NO_INTERACTION',
    'INTERACTION_STATE_IN_INTERACTION',
    'INTERACTION_STATE_END_OF_INTERACTION'
)
