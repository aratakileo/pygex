from pygex.color import colorValue, to_pygame_alpha_color
from pygame.font import FontType, get_init, init, Font

_font_buffer = {}


def get_pygame_font(font_or_size: FontType | int = 20):
    if not get_init():
        init()

    if isinstance(font_or_size, int):
        if font_or_size not in _font_buffer:
            _font_buffer[font_or_size] = Font(None, font_or_size)

        return _font_buffer[font_or_size]

    return font_or_size


def render_text(text, alpha_color: colorValue, font_or_size: FontType | int = 20, antialias=True):
    return get_pygame_font(font_or_size).render(text.__str__(), antialias, to_pygame_alpha_color(alpha_color))


def get_text_size(text, font_or_size: FontType | int = 20):
    return get_pygame_font(font_or_size).size(text.__str__())


__all__ = 'get_pygame_font', 'render_text', 'get_text_size'
