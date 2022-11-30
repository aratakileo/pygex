from pygex.color import colorValue, to_pygame_alpha_color
from pygame.font import FontType, get_init, init, Font
from pygex.image import AlphaSurface
from pygame.rect import Rect
from typing import Sequence

DEFAULT_FONT_SIZE = 20

ALIGN_LEFT = 0
ALIGN_RIGHT = 1
ALIGN_CENTER = 2
ALIGN_BLOCK = 3

_font_buffer = {}


def get_pygame_font(font_or_size: FontType | int = DEFAULT_FONT_SIZE):
    if not get_init():
        init()

    if isinstance(font_or_size, int):
        if font_or_size not in _font_buffer:
            _font_buffer[font_or_size] = Font(None, font_or_size)

        return _font_buffer[font_or_size]

    return font_or_size


def get_text_size(text, font_or_size: FontType | int = DEFAULT_FONT_SIZE):
    return get_pygame_font(font_or_size).size(text.__str__())


def render_text(text, color: colorValue, font_or_size: FontType | int = DEFAULT_FONT_SIZE, antialias=True):
    return get_pygame_font(font_or_size).render(text.__str__(), antialias, to_pygame_alpha_color(color))


def render_wrapped_text(
        text,
        color: colorValue,
        rect: Sequence | Rect,
        font_or_size: FontType | int = DEFAULT_FONT_SIZE,
        align=ALIGN_LEFT,
        line_spacing=0,
        lines: int = ...,
        antialias=True
):
    text = text.__str__().rstrip()
    color = to_pygame_alpha_color(color)

    if not text or lines is not ... and lines <= 0:
        return None

    font = get_pygame_font(font_or_size)
    textw = font.size(text)[0]
    is_single_line = '\n' not in text and (textw <= rect[2] or lines == 1)

    if (align == ALIGN_LEFT or align == ALIGN_BLOCK and ' ' not in text.strip()) and is_single_line:
        return font.render(text, antialias, color)

    output_surface = AlphaSurface(rect[2:])

    if is_single_line and align in (ALIGN_RIGHT, ALIGN_CENTER):
        if align == ALIGN_RIGHT:
            output_surface.blit(font.render(text, antialias, color), (rect[2] - textw, 0))
        else:
            output_surface.blit(font.render(text, antialias, color), ((rect[2] - textw) / 2, 0))

        return output_surface

    space_char_width, charh = font.size(' ')

    charh += line_spacing

    rendered_width = 0
    line_num = 0

    for line in text.split('\n'):
        for word in line.rstrip().split(' '):
            if not word:
                rendered_width += space_char_width
                continue

            wordw = font.size(word)[0]

            if rendered_width + wordw >= rect[2] and rendered_width > 0:
                line_num += 1

                if (line_num + 1) * charh - rect[3] > charh or lines is not ... and line_num == lines:
                    break

                rendered_width = 0

            if rendered_width == 0 and wordw > rect[2]:
                chars_in_line = int(rect[2] / (wordw / len(word)))
                chars_rendered = 0

                while chars_rendered < len(word):
                    chars_for_render = min(len(word) - chars_rendered, chars_in_line)

                    chars_surface = font.render(
                        word[chars_rendered: chars_rendered + chars_for_render],
                        antialias,
                        color
                    )

                    output_surface.blit(chars_surface, (0, line_num * charh))

                    rendered_width = chars_surface.get_width()
                    chars_rendered += chars_for_render
                    line_num += 1

                    if (line_num + 1) * charh - rect[3] > charh or lines is not ... and line_num == lines:
                        break

                line_num -= 1
            else:
                output_surface.blit(font.render(word, antialias, color), (rendered_width, line_num * charh))
                rendered_width += wordw

            rendered_width += space_char_width

        rendered_width = 0
        line_num += 1

        if line_num * charh - rect[3] > charh:
            break

    return output_surface


__all__ = (
    'DEFAULT_FONT_SIZE',
    'ALIGN_LEFT',
    'ALIGN_RIGHT',
    'ALIGN_CENTER',
    'ALIGN_BLOCK',
    'get_pygame_font',
    'get_text_size',
    'render_text',
    'render_wrapped_text'
)
