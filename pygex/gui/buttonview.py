from pygex.gui.view import SIZE_WRAP_CONTENT, DEFAULT_PADDING, GRAVITY_CENTER_HORIZONTAL, GRAVITY_CENTER_VERTICAL
from pygex.gui.drawable.interactiondrawable import InteractionDrawable, IS_NO_INTERACTION, IS_IN_INTERACTION
from pygame.constants import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygex.gui.drawable.interactiondrawable import IS_END_OF_INTERACTION
from pygex.gui.drawable.drawable import Drawable, ColorDrawable
from pygex.text import ALIGN_CENTER, DEFAULT_FONT_SIZE
from pygex.color import COLOR_TYPE, C_WHITE, C_GREEN
from pygame.mouse import get_pos as pg_mouse_get_pos
from pygex.gui.textview import TextView
from pygame.surface import SurfaceType
from pygame.font import FontType
from pygame.event import Event
from pygame.rect import Rect
from typing import Sequence


class ButtonView(TextView):
    def __init__(
            self,
            text: str = 'Click Me!',
            text_color: COLOR_TYPE = C_WHITE,
            size: Sequence[int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
            pos: Sequence[float | int] = (0, 0),
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity=GRAVITY_CENTER_HORIZONTAL | GRAVITY_CENTER_VERTICAL,
            text_align=ALIGN_CENTER,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | InteractionDrawable | COLOR_TYPE = InteractionDrawable(
                ColorDrawable(C_GREEN, 10)
            ),
            font_antialiasing=True,
            render_content_during_initialization=True
    ):
        super().__init__(
            text,
            text_color,
            size,
            pos,
            padding,
            content_gravity,
            text_align,
            text_line_spacing,
            text_lines_number,
            text_paragraph_space,
            font_or_font_size,
            background_drawable_or_color,
            font_antialiasing,
            render_content_during_initialization
        )

        self._background_drawable_is_interaction_drawable = isinstance(self._background_drawable, InteractionDrawable)
        self._interaction_status = IS_NO_INTERACTION
        self._focused = False

    def is_clicked(self):
        return self._interaction_status == IS_END_OF_INTERACTION

    def get_interaction_rect(self):
        return Rect(0, 0, 0, 0) if self._content_surface_buffer is None else Rect(
            self.x,
            self.y,
            self.get_background_width(),
            self.get_background_height(),
        )

    def process_event(self, e: Event):
        interaction_status_is_changed = False

        if e.type == MOUSEMOTION:
            self._focused = self.get_interaction_rect().collidepoint(pg_mouse_get_pos())
        elif e.type == MOUSEBUTTONDOWN and self._focused:
            self._interaction_status = IS_IN_INTERACTION
            interaction_status_is_changed = True
        elif e.type == MOUSEBUTTONUP and self._interaction_status == IS_IN_INTERACTION:
            self._interaction_status = IS_END_OF_INTERACTION if self._focused else IS_NO_INTERACTION
            interaction_status_is_changed = True

        if interaction_status_is_changed and self._background_drawable_is_interaction_drawable:
            self._background_drawable.set_interaction_status(self._interaction_status)

            if self._interaction_status == IS_IN_INTERACTION:
                self._background_surface_buffer = self._background_drawable.render(self.get_background_size())

    def flip(self):
        if self._interaction_status == IS_END_OF_INTERACTION:
            self._interaction_status = IS_NO_INTERACTION

            if self._background_drawable_is_interaction_drawable:
                self._background_drawable.set_interaction_status(self._interaction_status)

        if self._background_drawable_is_interaction_drawable:
            self._background_drawable.flip()

    def set_bg_drawable(self, drawable_or_color: Drawable | COLOR_TYPE):
        super().set_bg_drawable(drawable_or_color)

        self._background_drawable_is_interaction_drawable = isinstance(self._background_drawable, InteractionDrawable)

    def render(self, surface: SurfaceType):
        if self._background_drawable_is_interaction_drawable and self._background_drawable.is_need_to_be_rendered():
            self._background_surface_buffer = self._background_drawable.render(self.get_background_size())

        super().render(surface)


__all__ = 'ButtonView',
