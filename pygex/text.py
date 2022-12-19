from pygex.color import colorValue, to_pygame_alpha_color
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
            color: colorValue,
            size: Sequence[float | int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            align=ALIGN_LEFT,
            line_spacing: float | int = 0,
            lines_number: int = ...,
            paragraph_space: float | int = 0,
            antialias=True,
            strict_surface_size=False
    ):
        self._text = text
        self._color = color
        self._pygame_alpha_color = to_pygame_alpha_color(color)
        self._size = size
        self._font_or_font_size = font_or_font_size
        self._font = get_pygame_font(font_or_font_size)
        self._align = align
        self._line_spacing = line_spacing
        self._lines_number = lines_number
        self._paragraph_space = paragraph_space
        self._antialias = antialias
        self._strict_surface_size = strict_surface_size

        self._parsed_queue = ()
        self._parsed_text_size = 0, 0

        self.text_surface: SurfaceType | None = None

        self.parse_text()
        self.render()

    def get_render_size(self):
        return (
            self._size[0] if self._size[0] != SIZE_WRAP_CONTENT and self._strict_surface_size
            else self._parsed_text_size[0],

            self._size[1]
            if self._size[1] != SIZE_WRAP_CONTENT
               and (self._strict_surface_size or self._parsed_text_size[1] >= self._size[1])
            else self._parsed_text_size[1]
        )

    def parse_text(self):
        if not self._text or self._lines_number is not ... and self._lines_number <= 0 or self._paragraph_space < 0 \
                or self._size[0] != SIZE_WRAP_CONTENT and self._size[0] <= 0 \
                or self._size[1] != SIZE_WRAP_CONTENT and self._size[1] <= 0:
            return None

        font = get_pygame_font(self._font_or_font_size)
        char_height = font.get_height()

        max_lines_number = self._lines_number

        if self._lines_number is ... and self._size[1] != SIZE_WRAP_CONTENT:
            max_lines_number = int(self._size[1] / (char_height + self._line_spacing)) + 2

        parsed_queue = [0]
        char_index = 0
        line_number = 1
        text_piece = ''
        last_space_index = -1
        reserved_width = 0

        has_paragraph_space = True

        while char_index < len(self._text):
            if self._size[1] != SIZE_WRAP_CONTENT and line_number >= max_lines_number:
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

            if self._size[0] != SIZE_WRAP_CONTENT \
                    and font.size(text_piece + char)[0] > self._size[0] - self._paragraph_space * has_paragraph_space:
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
        self._parsed_text_size = reserved_width, line_number * char_height + (line_number - 1) * self._line_spacing

    def render(self):
        if not self._parsed_queue:
            return

        if len(self._parsed_queue) == 2 and self._align != ALIGN_BLOCK:
            self.render_as_singleline()
            return

        self.render_as_multiline()

    def render_as_singleline(self):
        """
        This method is not support align by block (`ALIGN_BLOCK`)
        """
        size = self.get_render_size()
        x = self._paragraph_space
        base_text_surface = self._font.render(self._text, self._antialias, self._pygame_alpha_color)

        if self._align == ALIGN_RIGHT:
            x = size[0] - base_text_surface.get_width() - x
        elif self._align == ALIGN_RIGHT:
            x = (size[0] - base_text_surface.get_width() + x) / 2

        self.text_surface = AlphaSurface(size)
        self.text_surface.blit(
            base_text_surface,
            (x, 0)
        )

    def render_as_multiline(self):
        size = self.get_render_size()
        self.text_surface = AlphaSurface(size)
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

            if self._align in (ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER) \
                    or ' ' not in segment or len(segment.split()) == 1:
                line_surface = self._font.render(segment, self._antialias, self._pygame_alpha_color)

                if self._align == ALIGN_RIGHT:
                    x = size[0] - line_surface.get_width() - offset_x
                elif self._align == ALIGN_CENTER:
                    x = (size[0] - line_surface.get_width() + offset_x) / 2
                else:
                    x = offset_x

                self.text_surface.blit(line_surface, (x, y))
            else:
                segment_pieces = segment.split(' ')
                space_width = (size[0] - offset_x - self._font.size(segment.replace(' ', ''))[0]) / segment.count(' ')
                spaces_number = 0

                x = offset_x

                for piece in segment_pieces:
                    if not piece:
                        spaces_number += 1
                        continue

                    x += spaces_number * space_width
                    piece_surface = self._font.render(piece, self._antialias, self._pygame_alpha_color)
                    self.text_surface.blit(piece_surface, (x, y))
                    x += piece_surface.get_width()

                    spaces_number = 1

            has_paragraph_space = False
            line_index += 1


def get_pygame_font(font_or_font_size: FontType | int = DEFAULT_FONT_SIZE):
    if not get_init():
        init()

    if isinstance(font_or_font_size, int):
        if font_or_font_size not in _font_buffer:
            _font_buffer[font_or_font_size] = Font(None, font_or_font_size)

        return _font_buffer[font_or_font_size]

    return font_or_font_size


def get_text_size(text: str, font_or_font_size: FontType | int = DEFAULT_FONT_SIZE):
    return get_pygame_font(font_or_font_size).size(text)


def render_text(text: str, color: colorValue, font_or_font_size: FontType | int = DEFAULT_FONT_SIZE, antialias=True):
    return get_pygame_font(font_or_font_size).render(text, antialias, to_pygame_alpha_color(color))


def parse_multiline_text(
        text: str,
        size: Sequence[float | int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
        font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
        line_spacing: float | int = 0,
        lines_number: int = ...,
        paragraph_space: float | int = 0
):
    if not text or lines_number is not ... and lines_number <= 0 or paragraph_space < 0 \
            or size[0] != SIZE_WRAP_CONTENT and size[0] <= 0 or size[1] != SIZE_WRAP_CONTENT and size[1] <= 0:
        return None

    font = get_pygame_font(font_or_font_size)
    char_height = font.get_height()

    max_lines_number = lines_number

    if lines_number is ... and size[1] != SIZE_WRAP_CONTENT:
        max_lines_number = int(size[1] / (char_height + line_spacing)) + 2

    parsed_queue = [0]
    char_index = 0
    line_number = 1
    text_piece = ''
    last_space_index = -1
    reserved_width = 0

    has_paragraph_space = True

    while char_index < len(text):
        if size[1] != SIZE_WRAP_CONTENT and line_number >= max_lines_number:
            break

        char = text[char_index]

        if char == '\n':
            if text_piece:
                reserved_width = max(reserved_width, font.size(text_piece)[0] + paragraph_space * has_paragraph_space)

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

        if size[0] != SIZE_WRAP_CONTENT \
                and font.size(text_piece + char)[0] > size[0] - paragraph_space * has_paragraph_space:
            if last_space_index > char_index - len(text_piece):
                expected_piece_len = len(text_piece)
                text_piece = text_piece[:last_space_index - char_index + len(text_piece) + 1]
                char_index -= expected_piece_len - len(text_piece)

            parsed_queue.append(text_piece)

            reserved_width = max(reserved_width, font.size(text_piece)[0] + paragraph_space * has_paragraph_space)
            has_paragraph_space = False
            text_piece = ''
            line_number += 1
            continue

        text_piece += char

        if char_index == len(text) - 1:
            parsed_queue.append(text_piece)

            reserved_width = max(reserved_width, font.size(text_piece)[0] + paragraph_space * has_paragraph_space)
            break

        char_index += 1

    if reserved_width == -1:
        reserved_width = font.size(text_piece)[0]

    return (*parsed_queue, ), (reserved_width, line_number * char_height + (line_number - 1) * line_spacing)


def render_parsed_multiline_text(
        parsed: tuple[tuple[int | str], tuple[int, int]],
        color: colorValue,
        size: Sequence[float | int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
        font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
        align=ALIGN_LEFT,
        line_spacing: float | int = 0,
        paragraph_space: float | int = 0,
        antialias=True
):
    size = (
        size[0] if size[0] != SIZE_WRAP_CONTENT else parsed[1][0],
        size[1] if size[1] != SIZE_WRAP_CONTENT else parsed[1][1]
    )

    text_surface = AlphaSurface(size)
    color = to_pygame_alpha_color(color)
    font = get_pygame_font(font_or_font_size)
    char_height = font.get_height()

    y = 0
    line_index = 0
    has_paragraph_space = True

    for segment in parsed[0]:
        if isinstance(segment, int):
            has_paragraph_space = True
            line_index += segment
            y += (char_height + line_spacing) * segment
            continue

        offset_x = paragraph_space * has_paragraph_space

        y += (char_height + line_spacing) * (line_index > 0)

        if align in (ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER) or ' ' not in segment or len(segment.split()) == 1:
            line_surface = font.render(segment, antialias, color)

            if align == ALIGN_RIGHT:
                x = size[0] - line_surface.get_width() - offset_x
            elif align == ALIGN_CENTER:
                x = (size[0] - line_surface.get_width() + offset_x) / 2
            else:
                x = offset_x

            text_surface.blit(line_surface, (x, y))
        else:
            segment_pieces = segment.split(' ')
            space_width = (size[0] - offset_x - font.size(segment.replace(' ', ''))[0]) / segment.count(' ')
            spaces_number = 0

            x = offset_x

            for piece in segment_pieces:
                if not piece:
                    spaces_number += 1
                    continue

                x += spaces_number * space_width
                piece_surface = font.render(piece, antialias, color)
                text_surface.blit(piece_surface, (x, y))
                x += piece_surface.get_width()

                spaces_number = 1

        has_paragraph_space = False
        line_index += 1

    return text_surface


__all__ = (
    'DEFAULT_FONT_SIZE',
    'ALIGN_LEFT',
    'ALIGN_RIGHT',
    'ALIGN_CENTER',
    'ALIGN_BLOCK',
    'SIZE_WRAP_CONTENT',
    'TextRenderer',
    'get_pygame_font',
    'get_text_size',
    'render_text',
    'parse_multiline_text',
    'render_parsed_multiline_text'
)
