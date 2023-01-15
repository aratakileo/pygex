from pygame import color as pg_color
from typing import Sequence

COLOR_TYPE = pg_color.Color | int | str | Sequence[int]


C_ABSOLUTE_RED = 0xff0000
C_ABSOLUTE_GREEN = 0x00ff00
C_ABSOLUTE_BLUE = 0x0000ff
C_BLACK = 0x000000
C_WHITE = 0xffffff
C_RED = 0xf44336
C_GREEN = 0x4caf50
C_BLUE = 0x2196f3
C_PINK = 0xe91e63
C_PURPLE = 0x9c27b0
C_DEEP_PURPLE = 0x673ab7
C_INDIGO = 0x3f51b5
C_LIGHT_BLUE = 0x03a9f4
C_CYAN = 0x00bcd4
C_TEAL = 0x009688
C_LIGHT_GREEN = 0x8bc34a
C_LIME = 0xcddc39
C_YELLOW = 0xffeb3b
C_AMBER = 0xffc107
C_ORANGE = 0xff9800
C_DEEP_ORANGE = 0xff5722
C_BROWN = 0x795548
C_BLUE_GREY = 0x607d8b
C_GREY = 0x9e9e9e
C_AQUA = 0x00ffff
C_AQUAMARINE = 0x7fffd4
C_AZURE = 0xf0ffff
C_BEIGE = 0xf5f5dc
C_BLUE_VIOLET = 0x8a2be2
C_CADET_BLUE = 0x5f9ea0
C_CHOCOLATE = 0xd2691e
C_CORAL = 0xff7f50
C_CRIMSON = 0xdc143c


def has_alpha(color: int):
    """
    Checking if color has alpha channel (works only for AHEX or HEX)
    :param color: alpha format AHEX or HEX
    """
    return color > 0xffffff


def get_alpha(color: int):
    """
    Checking if color has alpha channel (works only for AHEX or HEX)
    :param color: alpha format AHEX or HEX
    """
    return color >> 24


def set_alpha(color: int, alpha: int):
    """
    Checking if color has alpha channel (works only for AHEX or HEX)
    :param alpha: value from 0x00 to 0xff
    :param color: alpha format AHEX or HEX
    """
    return (alpha & 0xff) << 24 | color


def remove_alpha(color: int):
    """
    Checking if color has alpha channel (works only for AHEX or HEX)
    :param color: alpha format AHEX or HEX
    """
    return color & ~0xff000000


def from_hex(color: str):
    if color.startswith('#'):
        color = color[1:]

    return tuple(int(color[i:i+2], 16) for i in range(0, len(color), 2))


def rgb_to_hex(color: Sequence[int] | pg_color.Color):
    return (color[0] & 0xff) << 16 | (color[1] & 0xff) << 8 | (color[2] & 0xff)


def rgba_to_ahex(color: Sequence[int] | pg_color.Color):
    return (color[3] & 0xff) << 24 | rgb_to_hex(color)


def argb_to_ahex(color: Sequence[int] | pg_color.Color):
    return (color[0] & 0xff) << 24 | rgb_to_hex(color[1:])


def hex_to_hexa(color: int, alpha: int = 0xff):
    return color << 8 | alpha


def ahex_to_hexa(color: int):
    return remove_alpha(color) << 8 | get_alpha(color)


def ahex_to_rgba(color: int):
    return (color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff, (color >> 24) & 0xff


def color_as_int(color: COLOR_TYPE):
    if isinstance(color, Sequence):
        if len(color) == 3:
            return rgb_to_hex(color)

        if len(color) == 4:
            return rgba_to_ahex(color)

        return None

    if isinstance(color, str):
        if isinstance(color, str):
            if color.startswith('#'):
                if len(color) == 7:
                    return rgb_to_hex(from_hex(color))

                if len(color) == 9:
                    return rgba_to_ahex(from_hex(color))

                return None

            color = pg_color.Color(color)

    if isinstance(color, pg_color.Color):
        return rgba_to_ahex(color)

    return color


def invert(color: COLOR_TYPE, invert_alpha=False):
    """
    Invert the source color to inverse color.
    For example: black color will invert to white and white to black
    """
    color = color_as_int(color)

    if color is None:
        return None

    alpha = get_alpha(color)

    if invert_alpha:
        alpha = ~alpha & 0xff

    return set_alpha(~remove_alpha(color) & 0xffffff, alpha)


def to_gray(color: COLOR_TYPE):
    """
    Converts to specified color to shade of gray, based on which of shade of gray the specified color is closer to
    :param color: source color
    :return: shade of gray
    """
    color = color_as_int(color)

    if color is None:
        return None

    segment = (((color >> 16) & 0xff) * 299 + ((color >> 8) & 0xff) * 587 + (color & 0xff) * 114) // 1000

    return rgba_to_ahex((segment, segment, segment, get_alpha(color)))


def to_black_white(color: COLOR_TYPE):
    """
    Converts the specified color to black or white, based on which of them the specified color is closer to
    :param color: source color
    :return: black or white color
    """
    color = color_as_int(color)

    if color is None:
        return None

    segment = to_gray(color) & 0xff
    segment = 0x00 if segment < 0x7f else 0xff

    return rgba_to_ahex((segment, segment, segment, get_alpha(color)))


def to_readable_color(background_color: COLOR_TYPE):
    """
    Get a black or white color that will be clearly visible on the specified background color
    :param background_color: source color for analysis
    :return: black or white color
    """
    background_color = color_as_int(background_color)

    if background_color is None:
        return None

    return to_black_white(invert(background_color))


def to_pygame_alpha_color(color: COLOR_TYPE) -> tuple[int, int, int, int] | pg_color.Color | None:
    """
    Converting color from AHEX or HEX to HEXA (color format in pygame is HEXA)
    :param color: alpha format: AHEX, HEX, RGBA
    """
    if isinstance(color, int):
        if has_alpha(color):
            return ahex_to_rgba(color)

        return ahex_to_rgba(color | 0xff << 24)

    if isinstance(color, Sequence) and len(color) < 4:
        return *color, 255  # converting rgb to rgba

    if isinstance(color, str):
        if color.startswith('#'):
            if len(color) == 7:
                return from_hex(color)

            if len(color) == 9:
                return from_hex(color)

            return None

        return pg_color.Color(color)

    return color


__all__ = (
    'COLOR_TYPE',
    'C_ABSOLUTE_RED',
    'C_ABSOLUTE_GREEN',
    'C_ABSOLUTE_BLUE',
    'C_BLACK',
    'C_WHITE',
    'C_RED',
    'C_GREEN',
    'C_BLUE',
    'C_PINK',
    'C_PURPLE',
    'C_DEEP_PURPLE',
    'C_INDIGO',
    'C_LIGHT_BLUE',
    'C_CYAN',
    'C_TEAL',
    'C_LIGHT_GREEN',
    'C_LIME',
    'C_YELLOW',
    'C_AMBER',
    'C_ORANGE',
    'C_DEEP_ORANGE',
    'C_BROWN',
    'C_BLUE_GREY',
    'C_GREY',
    'C_AQUA',
    'C_AQUAMARINE',
    'C_AZURE',
    'C_BEIGE',
    'C_BLUE_VIOLET',
    'C_CADET_BLUE',
    'C_CHOCOLATE',
    'C_CORAL',
    'C_CRIMSON',
    'has_alpha',
    'get_alpha',
    'set_alpha',
    'from_hex',
    'rgb_to_hex',
    'rgba_to_ahex',
    'argb_to_ahex',
    'hex_to_hexa',
    'ahex_to_hexa',
    'ahex_to_rgba',
    'color_as_int',
    'invert',
    'to_gray',
    'to_black_white',
    'to_pygame_alpha_color',
    'to_readable_color'
)
