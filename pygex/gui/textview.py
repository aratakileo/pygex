from pygex.text import render_aligned_text, ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, ALIGN_BLOCK, DEFAULT_FONT_SIZE
from pygex.text import SIZE_WRAP_CONTENT
from pygame.surface import SurfaceType
from pygex.color import colorValue
from pygame.font import FontType
from typing import Sequence


class TextView:
    def __init__(
            self,
            text: str,
            size: Sequence[int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
            pos: Sequence[float | int] = (0, 0),
            text_color: colorValue = ...,
            text_align=ALIGN_LEFT,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            font_antialiasing=True
    ):
        self.padding = (8, 8, 8, 8)
        self.x, self.y = pos

        self._text = text
        self._width, self._height = size

        self._text_color = text_color
        self._text_align = text_align
        self._text_line_spacing = text_line_spacing
        self._text_lines_number = text_lines_number
        self._text_paragraph_space = text_paragraph_space

        self._font_antialiasing = font_antialiasing
        self._font_or_font_size = font_or_font_size

        self.__render_surface()

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value: Sequence[float | int]):
        self.x, self.y = value

    @property
    def size(self):
        return self._width, self._height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        old_width = self._width

        self._width = value

        if value != old_width:
            self.__render_surface()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value: int):
        old_height = self._height

        self._height = value

        if value != old_height:
            self.__render_surface()

    @size.setter
    def size(self, value: Sequence[int]):
        old_size = self._width, self._height

        self._width, self._height = value

        if value != old_size:
            self.__render_surface()

    @property
    def rendered_width(self):
        return self._surface_buffer.get_width() + self.padding[0] + self.padding[2]

    @property
    def rendered_height(self):
        return self._surface_buffer.get_height() + self.padding[1] + self.padding[3]

    @property
    def rendered_size(self):
        return self.rendered_width, self.rendered_height

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        old_text = self._text

        self._text = value

        if value != old_text:
            self.__render_surface()

    @property
    def text_align(self):
        return self._text_align

    @text_align.setter
    def text_align(self, value: int):
        old_text_align = self._text_align

        self._text_align = value

        if value != old_text_align:
            self.__render_surface()

    @property
    def text_color(self):
        return self._text_color if self._text_color is not ... else 0

    @text_color.setter
    def text_color(self, value: colorValue):
        old_text_color = self._text_color

        self._text_color = value

        if value != old_text_color:
            self.__render_surface()

    @property
    def font_or_font_size(self):
        return self._font_or_font_size

    @font_or_font_size.setter
    def font_or_font_size(self, value: FontType | int):
        old_font_or_font_size = self._font_or_font_size

        self._font_or_font_size = value

        if value != old_font_or_font_size:
            self.__render_surface()

    @property
    def text_line_spacing(self):
        return self._text_line_spacing

    @text_line_spacing.setter
    def text_line_spacing(self, value: float | int):
        old_text_line_spacing = self._text_line_spacing

        self._text_line_spacing = value

        if value != old_text_line_spacing:
            self.__render_surface()

    @property
    def text_lines_number(self):
        return self._text_lines_number

    @text_lines_number.setter
    def text_lines_number(self, value: float | int):
        old_text_lines_number = self._text_lines_number

        self._text_lines_number = value

        if value != old_text_lines_number:
            self.__render_surface()

    @property
    def text_paragraph_space(self):
        return self._text_paragraph_space

    @text_paragraph_space.setter
    def text_paragraph_space(self, value: float | int):
        old_text_paragraph_space = self._text_paragraph_space

        self._text_paragraph_space = value

        if value != old_text_paragraph_space:
            self.__render_surface()

    @property
    def font_antialiasing(self):
        return self._font_antialiasing

    @font_antialiasing.setter
    def font_antialiasing(self, value: float | int):
        old_font_antialiasing = self._font_antialiasing

        self._font_antialiasing = value

        if value != old_font_antialiasing:
            self.__render_surface()

    def __render_surface(self):
        self._surface_buffer = render_aligned_text(
            self._text,
            self.text_color,
            self._width, self._height,
            self._font_or_font_size,
            self._text_align
        )

    def render(self, surface: SurfaceType):
        surface.blit(self._surface_buffer, (self.x + self.padding[0], self.y + self.padding[1]))


__all__ = 'ALIGN_LEFT', 'ALIGN_RIGHT', 'ALIGN_CENTER', 'ALIGN_BLOCK', 'SIZE_WRAP_CONTENT', 'TextView',
