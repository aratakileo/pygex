from pygex.text import ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, ALIGN_BLOCK, DEFAULT_FONT_SIZE, TextRenderer
from pygex.gui.view import View, SIZE_WRAP_CONTENT, DEFAULT_PADDING, GRAVITY_LEFT, GRAVITY_TOP
from pygex.color import COLOR_TYPE, C_BLACK
from pygex.gui.drawable import Drawable
from pygame.font import FontType
from typing import Sequence


class TextView(View):
    def __init__(
            self,
            text: str,
            text_color: COLOR_TYPE = C_BLACK,
            size: Sequence[int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
            pos: Sequence[float | int] = (0, 0),
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity=GRAVITY_LEFT | GRAVITY_TOP,
            text_align=ALIGN_LEFT,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | COLOR_TYPE = ...,
            font_antialiasing=True,
            render_content_during_initialization=True
    ):
        super().__init__(size, pos, padding, content_gravity, background_drawable_or_color)

        self.text_renderer = TextRenderer(
            text,
            text_color,
            self.get_text_size(),
            font_or_font_size,
            text_align,
            text_line_spacing,
            text_lines_number,
            text_paragraph_space,
            font_antialiasing
        )

        if render_content_during_initialization:
            self.text_renderer.render()
            self._content_surface_buffer = self.text_renderer.text_surface

    def set_text(self, text: str):
        self.text_renderer.set_text(text)

        self._content_surface_buffer = self.text_renderer.text_surface

    def set_text_color(self, text_color: COLOR_TYPE):
        self.text_renderer.set_color(text_color)

        self._content_surface_buffer = self.text_renderer.text_surface

    def get_text_size(self):
        return (
            self._width if self._width == SIZE_WRAP_CONTENT
            else (self.get_background_width() - self._padding[0] - self._padding[2]),

            self._height if self._height == SIZE_WRAP_CONTENT
            else (self.get_background_height() - self._padding[1] - self._padding[3])
        )

    def apply_text_surface(self):
        self._content_surface_buffer = self.text_renderer.text_surface

    def render_content_surface(self):
        self.text_renderer.set_size(self.get_text_size())

        self._content_surface_buffer = self.text_renderer.text_surface


__all__ = 'ALIGN_LEFT', 'ALIGN_RIGHT', 'ALIGN_CENTER', 'ALIGN_BLOCK', 'TextView',
