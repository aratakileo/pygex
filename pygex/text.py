from pygex.color import colorValue, to_pygame_alpha_color
from pygame.font import FontType, get_init, init, Font


def render_text(
        text: any,
        alpha_color: colorValue,
        font_or_size: FontType | int = 20,
        antialias=True
):
    if not get_init():
        init()

    font = font_or_size

    if isinstance(font_or_size, int):
        font = Font(None, font_or_size)

    return font.render(text.__str__(), antialias, to_pygame_alpha_color(alpha_color))


__all__ = 'render_text'
