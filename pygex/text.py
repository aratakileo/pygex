from pygame.font import FontType, get_init, init, Font
from color import colorValue, to_pygame_alpha_color

_buffered_font: FontType | None = None
_buffered_font_size = -1


def render_text(
        text: any,
        alpha_color: colorValue,
        font_or_size: FontType | int = None,
        antialias=True
):
    if not get_init():
        init()

    font = font_or_size

    if isinstance(font_or_size, int):
        bufferize_font(font_or_size)

        font = _buffered_font
    elif font_or_size is None:
        if _buffered_font is None:
            bufferize_font(12)

        font = _buffered_font

    return font.render(text.__str__(), antialias, to_pygame_alpha_color(alpha_color))


def bufferize_font(size: int):
    if not get_init():
        init()

    global _buffered_font, _buffered_font_size

    if _buffered_font_size != size:
        _buffered_font_size = size
        _buffered_font = Font(None, size)


def get_buffered_font():
    return _buffered_font


__all__ = 'render_text', 'bufferize_font', 'get_buffered_font'
