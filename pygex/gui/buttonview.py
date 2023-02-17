from pygex.gui.view import SIZE_WRAP_CONTENT, DEFAULT_PADDING, GRAVITY_LEFT, GRAVITY_TOP
from pygame.constants import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygex.gui.drawable import Drawable, ColorDrawable
from pygex.text import ALIGN_LEFT, DEFAULT_FONT_SIZE
from pygex.color import COLOR_TYPE, C_WHITE, C_GREEN
from pygame.mouse import get_pos as pg_mouse_get_pos
from pygex.gui.textview import TextView
from pygame.font import FontType
from pygame.event import Event
from pygame.rect import Rect
from typing import Sequence


NO_INTERACTION = 0
START_INTERACTION = 1
END_INTERACTION = 2


class ButtonView(TextView):
    def __init__(
            self,
            text: str = 'Click Me!',
            text_color: COLOR_TYPE = C_WHITE,
            size: Sequence[int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
            pos: Sequence[float | int] = (0, 0),
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity=GRAVITY_LEFT | GRAVITY_TOP,
            text_align=ALIGN_LEFT,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | COLOR_TYPE = ColorDrawable(C_GREEN, 10),
            font_antialiasing=True
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
            font_antialiasing
        )

        self._interaction_status = NO_INTERACTION
        self._focused = False

    def is_clicked(self):
        return self._interaction_status == END_INTERACTION

    def get_interaction_rect(self):
        return Rect(0, 0, 0, 0) if self._content_surface_buffer is None else Rect(
            self.x,
            self.y,
            self.get_background_width(),
            self.get_background_height(),
        )

    def process_event(self, e: Event):
        if e.type == MOUSEMOTION:
            self._focused = self.get_interaction_rect().collidepoint(pg_mouse_get_pos())
        elif e.type == MOUSEBUTTONDOWN and self._focused:
            self._interaction_status = START_INTERACTION
        elif e.type == MOUSEBUTTONUP and self._interaction_status == START_INTERACTION:
            self._interaction_status = END_INTERACTION if self._focused else NO_INTERACTION

    def flip(self):
        if self._interaction_status == END_INTERACTION:
            self._interaction_status = NO_INTERACTION


__all__ = 'ButtonView',
