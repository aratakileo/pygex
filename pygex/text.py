from pygex.color import colorValue, to_pygame_alpha_color
from pygame.font import FontType, get_init, init, Font
from pygex.image import AlphaSurface
from typing import Sequence

DEFAULT_FONT_SIZE = 20

ALIGN_LEFT = 0
ALIGN_RIGHT = 1
ALIGN_CENTER = 2
ALIGN_BLOCK = 3

_font_buffer = {}


def get_pygame_font(font_or_font_size: FontType | int = DEFAULT_FONT_SIZE):
    if not get_init():
        init()

    if isinstance(font_or_font_size, int):
        if font_or_font_size not in _font_buffer:
            _font_buffer[font_or_font_size] = Font(None, font_or_font_size)

        return _font_buffer[font_or_font_size]

    return font_or_font_size


def get_text_size(text, font_or_font_size: FontType | int = DEFAULT_FONT_SIZE):
    return get_pygame_font(font_or_font_size).size(text.__str__())


def render_text(text, color: colorValue, font_or_font_size: FontType | int = DEFAULT_FONT_SIZE, antialias=True):
    return get_pygame_font(font_or_font_size).render(text.__str__(), antialias, to_pygame_alpha_color(color))


def render_aligned_text(
        text,
        color: colorValue,
        size_or_width: Sequence | float | int,
        font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
        align=ALIGN_LEFT,
        line_spacing: float | int = 0,
        lines_number: int = ...,
        paragraph_space: float | int = 0,
        antialias=True):
    text = text.__str__()

    if not text or lines_number is not ... and lines_number <= 0 or paragraph_space < 0:
        return None

    only_horizontal_limit = False

    if isinstance(size_or_width, int) or isinstance(size_or_width, float):
        only_horizontal_limit = True

    max_width = size_or_width if only_horizontal_limit else size_or_width[0]
    font = get_pygame_font(font_or_font_size)
    char_height = font.get_height() + line_spacing

    max_lines_number = lines_number

    if lines_number is ... and not only_horizontal_limit:
        max_lines_number = int(size_or_width[1] / char_height) + 2

    parsed_queue = [0]
    char_index = 0
    line_number = 1
    text_piece = ''
    last_space_index = -1

    while char_index < len(text):
        if not only_horizontal_limit and line_number >= max_lines_number:
            break

        char = text[char_index]

        if char == '\n':
            if text_piece:
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

        if font.size(text_piece + char)[0] > max_width - paragraph_space * isinstance(parsed_queue[-1], int):
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

    size = size_or_width if not only_horizontal_limit else (max_width, line_number * char_height)
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
    'get_pygame_font',
    'get_text_size',
    'render_text',
    'render_aligned_text'
)
