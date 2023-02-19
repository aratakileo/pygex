from pygex.color import COLOR_TYPE, to_pygame_alpha_color, C_BLACK, C_WHITE, ahex_to_rgba, color_as_int
from pygex.image import round_corners, AlphaSurface
from pygex.gui.drawable.drawable import Drawable
from pygame.draw import rect as pg_draw_rect
from pygame.surface import SurfaceType
from typing import Sequence


IS_NO_INTERACTION = 0
IS_IN_INTERACTION = 1
IS_END_OF_INTERACTION = 2


class InteractionDrawable(Drawable):
    def __init__(
            self,
            content: Drawable = None,
            effect_color: COLOR_TYPE = C_WHITE | 0x96000000,
            border_radius_or_radii: int | Sequence[int] = ...,
            border_width: int = 0,
            border_color: COLOR_TYPE = C_BLACK
    ):
        if border_radius_or_radii is ...:
            if content is None:
                border_radius_or_radii = -1
            else:
                border_radius_or_radii = content.radii

        super().__init__(border_radius_or_radii, border_width, border_color)

        self._effect_color = effect_color
        self._effect_color_rgba = ahex_to_rgba(color_as_int(effect_color))
        self._in_process_alpha_of_background = self._effect_color_rgba[-1]
        self._in_process_alpha_of_border = self._effect_color_rgba[-1]
        self._is_in_process = False
        self._interaction_status = IS_NO_INTERACTION

        self._content_drawable = content
        self._content_buffered_size = (-1, -1)
        self._content_buffered_surface: SurfaceType | None = None

        self.effect_border_width = 2
        self.effect_alpha_value_difference_for_start_decreasing_effect_border_alpha_value = 80
        self.effect_alpha_decreasing_per_frame = 3

    @property
    def is_need_to_be_rendered(self):
        return self._is_in_process

    @property
    def effect_color(self):
        return self._effect_color

    @effect_color.setter
    def effect_color(self, new_effect_color: COLOR_TYPE):
        self._effect_color = new_effect_color
        self._effect_color_rgba = ahex_to_rgba(color_as_int(new_effect_color))

    def get_content_drawable(self):
        return self._content_drawable

    def set_content_drawable(self, content: Drawable):
        self._content_drawable = content
        self._content_buffered_size = (-1, -1)

    def set_interaction_status(self, interaction_status: int, animate=True):
        if interaction_status == IS_NO_INTERACTION and self._interaction_status != IS_NO_INTERACTION and animate:
            self._is_in_process = True

        self._interaction_status = interaction_status
        self._in_process_alpha_of_background = self._effect_color_rgba[-1]
        self._in_process_alpha_of_border = self._effect_color_rgba[-1]

    def flip(self):
        """This method should be called every `flip()` call of custom View"""
        if self._is_in_process:
            if self._in_process_alpha_of_background > 0:
                self._in_process_alpha_of_background -= self.effect_alpha_decreasing_per_frame

            if self._in_process_alpha_of_background <= self._effect_color_rgba[-1] \
                    - self.effect_alpha_value_difference_for_start_decreasing_effect_border_alpha_value:
                self._in_process_alpha_of_border -= self.effect_alpha_decreasing_per_frame

        if self._in_process_alpha_of_border <= 0:
            self._is_in_process = False

    def render(self, size: Sequence[int]) -> SurfaceType | None:
        # STEP 1: rendering or getting content from buffer for the output surface
        if size != self._content_buffered_size:
            self._content_buffered_size = size
            self._content_buffered_surface = self._content_drawable.render(size)

        output_surface = self._content_buffered_surface.copy()

        # STEP 2: rendering effect on the output surface
        if self._interaction_status == IS_IN_INTERACTION:
            effect_surface = AlphaSurface(size)
            effect_surface.fill(to_pygame_alpha_color(self._effect_color))
            output_surface.blit(effect_surface, (0, 0))
        elif self._is_in_process:
            effect_surface = AlphaSurface(size)

            if self._in_process_alpha_of_background > 0:
                # ATTENTION: In this case, the method of simply filling in the Surface is used, and not drawing
                # a rounded rect, since the output Surface will be rounded later anyway
                effect_surface.fill((*self._effect_color_rgba[:3], self._in_process_alpha_of_background))

            # ATTENTION: this rect border (effect border) is rendered on a separate Surface, since when drawing rect
            # with a color with transparency, the method will simply replace the color in the Surface with
            # the specified color with transparency, and will not overlay it over the original Surface color
            pg_draw_rect(
                effect_surface,
                (*self._effect_color_rgba[:3], self._in_process_alpha_of_border),
                (0, 0, *size),
                self.effect_border_width,
                -1,
                self.border_top_left_radius,
                self.border_top_right_radius,
                self.border_bottom_left_radius,
                self.border_bottom_right_radius
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


__all__ = 'InteractionDrawable', 'IS_NO_INTERACTION', 'IS_IN_INTERACTION', 'IS_END_OF_INTERACTION'
