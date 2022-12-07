from pygex.text import render_aligned_text, ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, ALIGN_BLOCK, DEFAULT_FONT_SIZE
from pygex.gui.view import View, SIZE_WRAP_CONTENT, DEFAULT_PADDING
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
            text_align=ALIGN_LEFT,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | colorValue = ...,
            font_antialiasing=True
    ):
        super().__init__(size, pos, padding, background_drawable_or_color)

        self._text = text

        self._text_color = text_color
        self._text_align = text_align
        self._text_line_spacing = text_line_spacing
        self._text_lines_number = text_lines_number
        self._text_paragraph_space = text_paragraph_space

        self._font_antialiasing = font_antialiasing
        self._font_or_font_size = font_or_font_size

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        old_text = self._text

        self._text = value

        if value != old_text:
            self.__render_content_surface()
            self.__render_background_surface()

    @property
    def text_align(self):
        return self._text_align

    @text_align.setter
    def text_align(self, value: int):
        old_text_align = self._text_align

        self._text_align = value

        if value != old_text_align:
            self.__render_content_surface()
            self.__render_background_surface()

    @property
    def text_color(self):
        return self._text_color if self._text_color is not ... else 0

    @text_color.setter
    def text_color(self, value: colorValue):
        old_text_color = self._text_color

        self._text_color = value

        if value != old_text_color:
            self.__render_content_surface()

    @property
    def font_or_font_size(self):
        return self._font_or_font_size

    @font_or_font_size.setter
    def font_or_font_size(self, value: FontType | int):
        old_font_or_font_size = self._font_or_font_size

        self._font_or_font_size = value

        if value != old_font_or_font_size:
            self.__render_content_surface()
            self.__render_background_surface()

    @property
    def text_line_spacing(self):
        return self._text_line_spacing

    @text_line_spacing.setter
    def text_line_spacing(self, value: float | int):
        old_text_line_spacing = self._text_line_spacing

        self._text_line_spacing = value

        if value != old_text_line_spacing:
            self.__render_content_surface()
            self.__render_background_surface()

    @property
    def text_lines_number(self):
        return self._text_lines_number

    @text_lines_number.setter
    def text_lines_number(self, value: float | int):
        old_text_lines_number = self._text_lines_number

        self._text_lines_number = value

        if value != old_text_lines_number:
            self.__render_content_surface()
            self.__render_background_surface()

    @property
    def text_paragraph_space(self):
        return self._text_paragraph_space

    @text_paragraph_space.setter
    def text_paragraph_space(self, value: float | int):
        old_text_paragraph_space = self._text_paragraph_space

        self._text_paragraph_space = value

        if value != old_text_paragraph_space:
            self.__render_content_surface()
            self.__render_background_surface()

    @property
    def font_antialiasing(self):
        return self._font_antialiasing

    @font_antialiasing.setter
    def font_antialiasing(self, value: float | int):
        old_font_antialiasing = self._font_antialiasing

        self._font_antialiasing = value

        if value != old_font_antialiasing:
            self.__render_content_surface()

    def __render_content_surface(self):
        self._surface_buffer = render_aligned_text(
            self._text,
            self.text_color,
            self.size,
            self._font_or_font_size,
            self._text_align
        )


__all__ = 'ALIGN_LEFT', 'ALIGN_RIGHT', 'ALIGN_CENTER', 'ALIGN_BLOCK', 'TextView',
