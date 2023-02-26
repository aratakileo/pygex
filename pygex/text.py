from pygex.color import TYPE_COLOR, as_rgba
from pygame.font import FontType, get_init, init, Font
from pygame.surface import SurfaceType
from pygex.image import AlphaSurface
from typing import Sequence

DEFAULT_FONT_SIZE = 20

ALIGN_LEFT = 0
ALIGN_RIGHT = 1
ALIGN_CENTER = 2
ALIGN_BLOCK = 3

SIZE_WRAP_CONTENT = -2

_font_buffer = {}


class TextRenderer:
    def __init__(
            self,
            text: str,
            color: TYPE_COLOR,
            size: Sequence[int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            align=ALIGN_LEFT,
            line_spacing: float | int = 0,
            lines_number: int = ...,
            paragraph_space: float | int = 0,
            antialiasing=True,
            strict_surface_width=False
    ):
        self._text = text
        self._color = color
        self._pygame_color = as_rgba(color)
        self._width = SIZE_WRAP_CONTENT if size[0] == SIZE_WRAP_CONTENT else max(size[0], 0)
        self._height = SIZE_WRAP_CONTENT if size[1] == SIZE_WRAP_CONTENT else max(size[1], 0)
        self._font_or_font_size = font_or_font_size
        self._font = get_pygame_font(font_or_font_size)
        self._align = min(ALIGN_BLOCK, max(align, ALIGN_LEFT))
        self._line_spacing = line_spacing
        self._lines_number = lines_number if lines_number is ... else max(lines_number, 0)
        self._paragraph_space = max(paragraph_space, 0)
        self._antialiasing = antialiasing
        self._strict_surface_width = strict_surface_width

        self._parsed_queue = ()
        self._parsed_text_width = self._parsed_text_height = 0

        self.text_surface: SurfaceType | None = None

        self.parse_text()
        self.render()

    def set_text(self, text: str):
        old_text = self._text
        self._text = text

        if old_text != self._text:
            self.parse_text()
            self.render()

            return True

        return False

    def get_text(self):
        return self._text

    def set_color(self, color: TYPE_COLOR):
        old_pygame_alpha_color = self._pygame_color
        self._color = color
        self._pygame_color = as_rgba(color)

        if old_pygame_alpha_color != self._pygame_color:
            self.render()

    def get_color(self) -> TYPE_COLOR:
        return self._color

    def get_pygame_color(self) -> tuple[int, int, int, int]:
        return self._pygame_color

    def set_size(self, size: Sequence[int]):
        old_size = self._width, self._height
        self._width = SIZE_WRAP_CONTENT if size[0] == SIZE_WRAP_CONTENT else max(size[0], 0)
        self._height = SIZE_WRAP_CONTENT if size[1] == SIZE_WRAP_CONTENT else max(size[1], 0)

        if old_size != (self._width, self._height):
            self.parse_text()
            self.render()

    def get_size(self) -> tuple[int, int]:
        return self._width, self._height

    def set_width(self, width: int):
        old_width = self._width
        self._width = SIZE_WRAP_CONTENT if width == SIZE_WRAP_CONTENT else max(width, 0)

        if old_width != self._width:
            self.parse_text()
            self.render()

    def get_width(self) -> int:
        return self._width

    def set_height(self, height: int):
        old_height = self._height
        self._height = SIZE_WRAP_CONTENT if height == SIZE_WRAP_CONTENT else max(height, 0)

        if old_height != self._height:
            self.parse_text()
            self.render()

    def get_height(self) -> int:
        return self._height

    def set_font_or_font_size(self, font_or_font_size: FontType | int):
        old_font = self._font
        self._font_or_font_size = font_or_font_size
        self._font = get_pygame_font(font_or_font_size)

        if old_font != self._font:
            self.parse_text()
            self.render()

    def get_font_or_font_size(self):
        return self._font_or_font_size

    def get_font(self):
        return self._font

    def set_align(self, align: int):
        old_align = self._align
        self._align = min(ALIGN_BLOCK, max(align, ALIGN_LEFT))

        if old_align != self._align:
            self.render()

    def get_align(self):
        return self._align

    def set_line_spacing(self, line_spacing: float | int):
        old_line_spacing = self._line_spacing
        self._line_spacing = line_spacing

        if old_line_spacing == self._line_spacing:
            return

        if self._line_spacing > old_line_spacing:
            self.render()
            return

        self.parse_text()
        self.render()

    def get_line_spacing(self):
        return self._line_spacing

    def set_lines_number(self, lines_number: int):
        old_lines_number = self._lines_number
        self._lines_number = lines_number if lines_number is ... else max(lines_number, 0)

        if old_lines_number == self._lines_number:
            return

        if self._lines_number < old_lines_number:
            self.render()
            return

        self.parse_text()
        self.render()

    def get_lines_number(self):
        return self._lines_number

    def set_paragraph_space(self, paragraph_space: float | int):
        old_paragraph_space = self._paragraph_space
        self._paragraph_space = max(paragraph_space, 0)

        if old_paragraph_space != self._paragraph_space:
            self.parse_text()
            self.render()

    def get_paragraph_space(self):
        return self._paragraph_space

    def set_antialiasing(self, antialiasing: bool):
        old_antialiasing = self._antialiasing
        self._antialiasing = antialiasing

        if old_antialiasing != antialiasing:
            self.render()

    def is_antialiasing(self):
        return self._antialiasing

    def set_strict_surface_width(self, strict_surface_width: bool):
        old_strict_surface_width = self._strict_surface_width
        self._strict_surface_width = strict_surface_width

        if old_strict_surface_width != strict_surface_width:
            self.render()

    def is_strict_surface_width(self):
        return self._strict_surface_width

    def get_render_size(self):
        return (
            self._width if self._width != SIZE_WRAP_CONTENT and self._strict_surface_width
            else self._parsed_text_width,

            self._height
            if self._height != SIZE_WRAP_CONTENT
            and (self._strict_surface_width or self._parsed_text_height >= self._height)
            else self._parsed_text_height
        )

    def parse_text(self):
        if not self._text or self._lines_number == 0:
            self._parsed_queue = ()
            self._parsed_text_width = self._parsed_text_height = 0
            return

        font = get_pygame_font(self._font_or_font_size)
        char_height = font.get_height()

        max_lines_number = self._lines_number

        if self._lines_number is ... and self._height != SIZE_WRAP_CONTENT:
            max_lines_number = int(self._height / (char_height + self._line_spacing)) + 2

        parsed_queue = [0]
        char_index = 0
        line_number = 1
        text_piece = ''
        last_space_index = -1
        reserved_width = 0

        has_paragraph_space = True

        while char_index < len(self._text):
            if self._height != SIZE_WRAP_CONTENT and line_number >= max_lines_number:
                break

            char = self._text[char_index]

            if char == '\n':
                if text_piece:
                    reserved_width = max(reserved_width,
                                         font.size(text_piece)[0] + self._paragraph_space * has_paragraph_space)

                    parsed_queue.append(text_piece)
                    parsed_queue.append(0)
                elif isinstance(parsed_queue[-1], int):
                    parsed_queue[-1] += 1

                line_number += 1
                char_index += 1
                text_piece = ''
                has_paragraph_space = True
                continue

            if char == ' ':
                last_space_index = char_index

            if self._width != SIZE_WRAP_CONTENT \
                    and font.size(text_piece + char)[0] > self._width - self._paragraph_space * has_paragraph_space:
                if last_space_index > char_index - len(text_piece):
                    expected_piece_len = len(text_piece)
                    text_piece = text_piece[:last_space_index - char_index + len(text_piece) + 1]
                    char_index -= expected_piece_len - len(text_piece)

                parsed_queue.append(text_piece)

                reserved_width = max(
                    reserved_width,
                    font.size(text_piece)[0] + self._paragraph_space * has_paragraph_space
                )
                has_paragraph_space = False
                text_piece = ''
                line_number += 1
                continue

            text_piece += char

            if char_index == len(self._text) - 1:
                parsed_queue.append(text_piece)

                reserved_width = max(
                    reserved_width,
                    font.size(text_piece)[0] + self._paragraph_space * has_paragraph_space
                )
                break

            char_index += 1

        if reserved_width == -1:
            reserved_width = font.size(text_piece)[0]

        self._parsed_queue = *parsed_queue,
        self._parsed_text_width = reserved_width
        self._parsed_text_height = line_number * char_height + (line_number - 1) * self._line_spacing

    def render(self):
        if not self._parsed_queue:
            self.text_surface = None
            return

        if self._lines_number == 1 or len(self._parsed_queue) == 2 \
                or len(self._parsed_queue) == 3 and isinstance(self._parsed_queue[-1], int):
            self.render_as_singleline_content()
            return

        self.render_as_multiline_content()

    def render_as_singleline_content(self):
        """This method is faster for the single line content"""
        if not self._parsed_queue:
            self.text_surface = None
            return

        renderw, renderh = self.get_render_size()
        text = self._text.strip('\n')
        y = self._parsed_queue[0] * (self._font.get_height() + self._line_spacing)

        self.text_surface = AlphaSurface((renderw, renderh))

        if self._align != ALIGN_BLOCK or ' ' not in text or len(text.split()) == 1:
            base_text_surface = self._font.render(text, self._antialiasing, self._pygame_color)

            if self._align == ALIGN_RIGHT:
                x = renderw - base_text_surface.get_width() - self._paragraph_space
            elif self._align == ALIGN_CENTER:
                x = (renderw - base_text_surface.get_width() + self._paragraph_space) / 2
            else:
                x = self._paragraph_space

            self.text_surface.blit(
                base_text_surface,
                (x, y)
            )
        else:
            segment_pieces = text.split(' ')
            space_width = (
                                  renderw - self._paragraph_space - self._font.size(text.replace(' ', ''))[0]
                          ) / text.count(' ')
            spaces_number = 0

            x = self._paragraph_space

            for piece in segment_pieces:
                if not piece:
                    spaces_number += 1
                    continue

                x += spaces_number * space_width
                piece_surface = self._font.render(piece, self._antialiasing, self._pygame_color)
                self.text_surface.blit(piece_surface, (x, y))
                x += piece_surface.get_width()

                spaces_number = 1

    def render_as_multiline_content(self):
        """This method is not optimized for the single line content"""
        if not self._parsed_queue:
            self.text_surface = None
            return

        renderw, renderh = self.get_render_size()
        self.text_surface = AlphaSurface((renderw, renderh))
        char_height = self._font.get_height()

        y = 0
        line_index = 0
        has_paragraph_space = True

        for segment in self._parsed_queue:
            if isinstance(segment, int):
                has_paragraph_space = True
                line_index += segment
                y += (char_height + self._line_spacing) * segment
                continue

            offset_x = self._paragraph_space * has_paragraph_space

            y += (char_height + self._line_spacing) * (line_index > 0)

            if self._align != ALIGN_BLOCK or ' ' not in segment or len(segment.split()) == 1:
                line_surface = self._font.render(segment, self._antialiasing, self._pygame_color)

                if self._align == ALIGN_RIGHT:
                    x = renderw - line_surface.get_width() - offset_x
                elif self._align == ALIGN_CENTER:
                    x = (renderw - line_surface.get_width() + offset_x) / 2
                else:
                    x = offset_x

                self.text_surface.blit(line_surface, (x, y))
            else:
                segment_pieces = segment.split(' ')
                space_width = (renderw - offset_x - self._font.size(segment.replace(' ', ''))[0]) / segment.count(' ')
                spaces_number = 0

                x = offset_x

                for piece in segment_pieces:
                    if not piece:
                        spaces_number += 1
                        continue

                    x += spaces_number * space_width
                    piece_surface = self._font.render(piece, self._antialiasing, self._pygame_color)
                    self.text_surface.blit(piece_surface, (x, y))
                    x += piece_surface.get_width()

                    spaces_number = 1

            has_paragraph_space = False
            line_index += 1


def get_pygame_font(font_or_font_size: FontType | int = DEFAULT_FONT_SIZE):
    if not get_init():
        init()

    if isinstance(font_or_font_size, int):
        font_or_font_size = max(font_or_font_size, 1)

        if font_or_font_size not in _font_buffer:
            _font_buffer[font_or_font_size] = Font(None, font_or_font_size)

        return _font_buffer[font_or_font_size]

    return font_or_font_size


def render_text(text: str, color: TYPE_COLOR, font_or_font_size: FontType | int = DEFAULT_FONT_SIZE, antialiasing=True):
    return get_pygame_font(font_or_font_size).render(text, antialiasing, as_rgba(color))


__all__ = (
    'DEFAULT_FONT_SIZE',
    'ALIGN_LEFT',
    'ALIGN_RIGHT',
    'ALIGN_CENTER',
    'ALIGN_BLOCK',
    'SIZE_WRAP_CONTENT',
    'TextRenderer',
    'get_pygame_font',
    'render_text'
)
