from pygex.gui.view import View, SIZE_WRAP_CONTENT, DEFAULT_PADDING, GRAVITY_LEFT, GRAVITY_TOP
from pygex.text import ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, ALIGN_BLOCK, DEFAULT_FONT_SIZE
from pygex.text import parse_multiline_text, render_parsed_multiline_text
from pygex.gui.drawable import Drawable
from pygex.color import colorValue
from pygame.font import FontType
from typing import Sequence


class TextView(View):
    def __init__(
            self,
            text: str,
            text_color: colorValue = ...,
            size: Sequence[int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
            pos: Sequence[float | int] = (0, 0),
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity=GRAVITY_LEFT | GRAVITY_TOP,
            text_align=ALIGN_LEFT,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | colorValue = ...,
            font_antialiasing=True
    ):
        super().__init__(size, pos, padding, content_gravity, background_drawable_or_color)

        self._text = text
        self._formatted_text = None

        self._text_color = text_color
        self._text_align = text_align
        self._text_line_spacing = text_line_spacing
        self._text_lines_number = text_lines_number
        self._text_paragraph_space = text_paragraph_space

        self._font_antialiasing = font_antialiasing
        self._font_or_font_size = font_or_font_size

        self.parse_text()

    @property
    def text(self):
        return self._text if self._formatted_text is None else self._formatted_text

    @text.setter
    def text(self, value: str):
        old_text = self._text

        self._text = value

        if value != old_text:
            self._formatted_text = None
            self.render_content_surface()
            self.render_background_surface()

    @property
    def text_align(self):
        return self._text_align

    @text_align.setter
    def text_align(self, value: int):
        old_text_align = self._text_align

        self._text_align = value

        if value != old_text_align:
            self.render_text()

    @property
    def text_color(self):
        return self._text_color if self._text_color is not ... else 0

    @text_color.setter
    def text_color(self, value: colorValue):
        old_text_color = self._text_color

        self._text_color = value

        if value != old_text_color:
            self.render_text()

    @property
    def font_or_font_size(self):
        return self._font_or_font_size

    @font_or_font_size.setter
    def font_or_font_size(self, value: FontType | int):
        old_font_or_font_size = self._font_or_font_size

        self._font_or_font_size = value

        if value != old_font_or_font_size:
            self.render_content_surface()
            self.render_background_surface()

    @property
    def text_line_spacing(self):
        return self._text_line_spacing

    @text_line_spacing.setter
    def text_line_spacing(self, value: float | int):
        old_text_line_spacing = self._text_line_spacing

        self._text_line_spacing = value

        if value != old_text_line_spacing:
            self.render_content_surface()
            self.render_background_surface()

    @property
    def text_lines_number(self):
        return self._text_lines_number

    @text_lines_number.setter
    def text_lines_number(self, value: float | int):
        old_text_lines_number = self._text_lines_number

        self._text_lines_number = value

        if value != old_text_lines_number:
            self.render_content_surface()
            self.render_background_surface()

    @property
    def text_paragraph_space(self):
        return self._text_paragraph_space

    @text_paragraph_space.setter
    def text_paragraph_space(self, value: float | int):
        old_text_paragraph_space = self._text_paragraph_space

        self._text_paragraph_space = value

        if value != old_text_paragraph_space:
            self.render_content_surface()
            self.render_background_surface()

    @property
    def font_antialiasing(self):
        return self._font_antialiasing

    @font_antialiasing.setter
    def font_antialiasing(self, value: float | int):
        old_font_antialiasing = self._font_antialiasing

        self._font_antialiasing = value

        if value != old_font_antialiasing:
            self.render_text()

    def format_text(self, *args):
        self._formatted_text = self._text % args

        self.render_content_surface()
        self.render_background_surface()

    def parse_text(self):
        width = self._width if self._width == SIZE_WRAP_CONTENT \
            else (self.background_width - self._padding[0] - self._padding[2])
        height = self._height if self._height == SIZE_WRAP_CONTENT \
            else (self.background_height - self._padding[1] - self._padding[3])

        self._parsed_text = parse_multiline_text(
            self.text,
            (width, height),
            self._font_or_font_size,
            self._text_line_spacing,
            self._text_lines_number,
            self._text_paragraph_space
        )

    def render_text(self):
        self._content_surface_buffer = render_parsed_multiline_text(
            self._parsed_text,
            self.text_color,
            self._parsed_text[1],
            self._font_or_font_size,
            self._text_align,
            self._text_line_spacing,
            self._text_paragraph_space,
            self._font_antialiasing
        )

    def render_content_surface(self):
        self.parse_text()
        self.render_text()


__all__ = 'ALIGN_LEFT', 'ALIGN_RIGHT', 'ALIGN_CENTER', 'ALIGN_BLOCK', 'TextView',
