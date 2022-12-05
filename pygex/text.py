from pygex.color import colorValue, to_pygame_alpha_color
from pygame.font import FontType, get_init, init, Font
from pygex.image import AlphaSurface
from typing import Sequence

DEFAULT_FONT_SIZE = 20

ALIGN_LEFT = 0
ALIGN_RIGHT = 1
ALIGN_CENTER = 2
ALIGN_BLOCK = 3

SIZE_WRAP_CONTENT = -2

_font_buffer = {}


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


def render_aligned_text(
        text: str,
        color: colorValue,
        size: Sequence[float | int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
        font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
        align=ALIGN_LEFT,
        line_spacing: float | int = 0,
        lines_number: int = ...,
        paragraph_space: float | int = 0,
        antialias=True):
    if not text or lines_number is not ... and lines_number <= 0 or paragraph_space < 0 \
            or size[0] != SIZE_WRAP_CONTENT and size[0] <= 0 or size[1] != SIZE_WRAP_CONTENT and size[1] <= 0:
        return None

    font = get_pygame_font(font_or_font_size)
    char_height = font.get_height() + line_spacing

    max_lines_number = lines_number

    if lines_number is ... and size[1] != SIZE_WRAP_CONTENT:
        max_lines_number = int(size[1] / char_height) + 2

    parsed_queue = [0]
    char_index = 0
    line_number = 1
    text_piece = ''
    last_space_index = -1
    max_width = -1

    while char_index < len(text):
        if size[1] != SIZE_WRAP_CONTENT and line_number >= max_lines_number:
            break

        char = text[char_index]

        if char == '\n':
            if text_piece:
                if size[0] == SIZE_WRAP_CONTENT:
                    max_width = max(max_width, font.size(text_piece)[0])

                parsed_queue.append(text_piece)
                parsed_queue.append(0)
            elif isinstance(parsed_queue[-1], int):
                parsed_queue[-1] += 1

            line_number += 1
            text_piece = ''
            char_index += 1
            continue

        if char == ' ':
            last_space_index = char_index

        if size[0] != SIZE_WRAP_CONTENT \
                and font.size(text_piece + char)[0] > size[0] - paragraph_space * isinstance(parsed_queue[-1], int):
            if last_space_index > char_index - len(text_piece):
                expected_piece_len = len(text_piece)
                text_piece = text_piece[:last_space_index - char_index + len(text_piece) + 1]
                char_index -= expected_piece_len - len(text_piece)

            parsed_queue.append(text_piece)

            text_piece = ''
            line_number += 1
            continue

        text_piece += char

        if char_index == len(text) - 1:
            parsed_queue.append(text_piece)
            break

        char_index += 1

    if max_width == -1 and size[0] == SIZE_WRAP_CONTENT:
        max_width = font.size(text_piece)[0]

    size = (
        size[0] if size[0] != SIZE_WRAP_CONTENT else max_width,
        size[1] if size[1] != SIZE_WRAP_CONTENT else line_number * char_height
    )

    text_surface = AlphaSurface(size)
    color = to_pygame_alpha_color(color)

    line_number = 0
    has_paragraph_space = True

    for segment in parsed_queue:
        if isinstance(segment, int):
            has_paragraph_space = True
            line_number += segment
            continue

        offset_x = paragraph_space * has_paragraph_space

        y = char_height * line_number

        if align in (ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER) or ' ' not in segment or len(segment.split()) == 1:
            line_surface = font.render(segment, antialias, color)

            if align == ALIGN_RIGHT:
                x = size[0] - line_surface.get_width() - offset_x
            elif align == ALIGN_CENTER:
                x = (size[0] - line_surface.get_width()) / 2 + offset_x
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
        line_number += 1

    return text_surface


__all__ = (
    'DEFAULT_FONT_SIZE',
    'ALIGN_LEFT',
    'ALIGN_RIGHT',
    'ALIGN_CENTER',
    'ALIGN_BLOCK',
    'SIZE_WRAP_CONTENT',
    'get_pygame_font',
    'get_text_size',
    'render_text',
    'render_aligned_text'
)
