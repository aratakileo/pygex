from pygame import color as pg_color
from typing import Sequence

TYPE_COLOR = pg_color.Color | int | str | Sequence[int]


COLOR_ABSOLUTE_RED = 0xff0000
COLOR_ABSOLUTE_GREEN = 0x00ff00
COLOR_ABSOLUTE_BLUE = 0x0000ff
COLOR_ABSOLUTE_LIGHT_BLUE = 0x00ffff
COLOR_ABSOLUTE_PINK = 0xff00ff
COLOR_ABSOLUTE_YELLOW = 0xffff00

COLOR_BLACK = 0x000000
COLOR_WHITE = 0xffffff
COLOR_RED = 0xf44336
COLOR_GREEN = 0x4caf50
COLOR_BLUE = 0x2196f3
COLOR_PINK = 0xe91e63
COLOR_PURPLE = 0x9c27b0
COLOR_DEEP_PURPLE = 0x673ab7
COLOR_INDIGO = 0x3f51b5
COLOR_LIGHT_BLUE = 0x03a9f4
COLOR_CYAN = 0x00bcd4
COLOR_TEAL = 0x009688
COLOR_LIGHT_GREEN = 0x8bc34a
COLOR_LIME = 0xcddc39
COLOR_YELLOW = 0xffeb3b
COLOR_AMBER = 0xffc107
COLOR_ORANGE = 0xff9800
COLOR_DEEP_ORANGE = 0xff5722
COLOR_BROWN = 0x795548
COLOR_BLUE_GREY = 0x607d8b
COLOR_GREY = 0x9e9e9e
COLOR_AQUA = 0x00ffff
COLOR_AQUAMARINE = 0x7fffd4
COLOR_AZURE = 0xf0ffff
COLOR_BEIGE = 0xf5f5dc
COLOR_BLUE_VIOLET = 0x8a2be2
COLOR_CADET_BLUE = 0x5f9ea0
COLOR_CHOCOLATE = 0xd2691e
COLOR_CORAL = 0xff7f50
COLOR_CRIMSON = 0xdc143c


COLOR_TRANSPARENT = -1
"""
This color means that the element for which it was used is transparent, and at the code level, with some exceptions,
an element of this color is simply not rendered. This color exists only in AHEX format and if try to convert
to other formats, such as RGBA, HEXA, etc., then nothing will come out and the value None will be returned.
"""


class GRADIENT_WITCHING_HOUR:
    FIRST_COLOR = 0xc31432
    LAST_COLOR = 0x240b36

    TUPLE = (FIRST_COLOR, LAST_COLOR)


class GRADIENT_WIRETAP:
    FIRST_COLOR = 0x8a2387
    MIDDLE_COLOR = 0xe94057
    LAST_COLOR = 0xf27121

    TUPLE = (FIRST_COLOR, MIDDLE_COLOR, LAST_COLOR)


class GRADIENT_RASTAFARI:
    FIRST_COLOR = 0x1e9600
    MIDDLE_COLOR = 0xfff200
    LAST_COLOR = COLOR_ABSOLUTE_RED

    TUPLE = (FIRST_COLOR, MIDDLE_COLOR, LAST_COLOR)


class GRADIENT_JSHINE:
    FIRST_COLOR = 0x12c2e9
    MIDDLE_COLOR = 0xc471ed
    LAST_COLOR = 0xf64f59

    TUPLE = (FIRST_COLOR, MIDDLE_COLOR, LAST_COLOR)


def has_alpha(color: int):
    """
    Checking if color has alpha channel (works only for AHEX or HEX)
    :param color: alpha format AHEX or HEX
    """
    if color == COLOR_TRANSPARENT:
        return False

    return color > 0xffffff


def get_alpha(color: int):
    """
    Checking if color has alpha channel (works only for AHEX or HEX)
    :param color: alpha format AHEX or HEX
    """
    if color == COLOR_TRANSPARENT:
        return 0

    return color >> 24


def set_alpha(color: int, alpha: int):
    """
    Checking if color has alpha channel (works only for AHEX or HEX)
    :param alpha: value from 0x00 to 0xff
    :param color: alpha format AHEX or HEX
    """
    if color == COLOR_TRANSPARENT:
        return COLOR_TRANSPARENT

    return (alpha & 0xff) << 24 | color


def remove_alpha(color: int):
    """
    Checking if color has alpha channel (works only for AHEX or HEX)
    :param color: alpha format AHEX or HEX
    """
    if color == COLOR_TRANSPARENT:
        return COLOR_TRANSPARENT

    return color & ~0xff000000


def replace_alpha(color: int, new_alpha: int):
    return (color & ~0xff000000) | (new_alpha & 0xff) << 24


def parse_hex(color: str):
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
    if color == COLOR_TRANSPARENT:
        return COLOR_TRANSPARENT

    return color << 8 | alpha


def ahex_to_hexa(color: int):
    if color == COLOR_TRANSPARENT:
        return

    return remove_alpha(color) << 8 | get_alpha(color)


def ahex_to_rgba(color: int):
    if color == COLOR_TRANSPARENT:
        return

    return (color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff, (color >> 24) & 0xff


def invert(color: TYPE_COLOR, invert_alpha=False):
    """
    Invert the source color to inverse color.
    For example: black color will invert to white and white to black
    """
    color = as_ahex(color)

    if color is None:
        return

    if color == COLOR_TRANSPARENT:
        return COLOR_TRANSPARENT

    alpha = get_alpha(color)

    if invert_alpha:
        alpha = ~alpha & 0xff

    return set_alpha(~remove_alpha(color) & 0xffffff, alpha)


def to_gray(color: TYPE_COLOR):
    """
    Converts to specified color to shade of gray, based on which of shade of gray the specified color is closer to
    :param color: source color
    :return: shade of gray
    """
    color = as_ahex(color)

    if color is None:
        return

    if color == COLOR_TRANSPARENT:
        return COLOR_TRANSPARENT

    segment = (((color >> 16) & 0xff) * 299 + ((color >> 8) & 0xff) * 587 + (color & 0xff) * 114) // 1000

    return rgba_to_ahex((segment, segment, segment, get_alpha(color)))


def to_black_white(color: TYPE_COLOR):
    """
    Converts the specified color to black or white, based on which of them the specified color is closer to
    :param color: source color
    :return: black or white color
    """
    color = as_ahex(color)

    if color is None:
        return

    if color == COLOR_TRANSPARENT:
        return COLOR_TRANSPARENT

    segment = to_gray(color) & 0xff
    segment = 0x00 if segment < 0x7f else 0xff

    return rgba_to_ahex((segment, segment, segment, get_alpha(color)))


def to_readable_color(background_color: TYPE_COLOR):
    """
    Get a black or white color that will be clearly visible on the specified background color
    :param background_color: source color for analysis
    :return: black or white color
    """
    background_color = as_ahex(background_color)

    if background_color is None:
        return

    if background_color == COLOR_TRANSPARENT:
        return COLOR_TRANSPARENT

    return to_black_white(invert(background_color))


def as_ahex(color: TYPE_COLOR):
    """
    This function can be used for converting any color to supportable color for pygex
    :param color: any of: AHEX, HEX, RGBA, pygame.Color
    :return: AHEX as int
    """
    if isinstance(color, Sequence):
        if len(color) == 3:
            return rgb_to_hex(color)

        if len(color) == 4:
            return rgba_to_ahex(color)

        return

    if isinstance(color, str):
        if isinstance(color, str):
            if color.startswith('#'):
                if len(color) == 7:
                    return rgb_to_hex(parse_hex(color))

                if len(color) == 9:
                    return rgba_to_ahex(parse_hex(color))

                return

            color = pg_color.Color(color)

    if isinstance(color, pg_color.Color):
        return rgba_to_ahex(color)

    return color


def as_rgba(color: TYPE_COLOR) -> tuple[int, int, int, int] | pg_color.Color | None:
    """
    This function can be used for converting any color to supportable color for pygame
    :param color: any of: AHEX, HEX, RGBA, pygame.Color
    :return: RGBA as tuple or pygame.Color
    """
    if isinstance(color, int):
        if color == COLOR_TRANSPARENT:
            return

        if has_alpha(color):
            return ahex_to_rgba(color)

        return ahex_to_rgba(color | 0xff << 24)

    if isinstance(color, Sequence) and len(color) < 4:
        return *color, 0xff  # converting rgb to rgba

    if isinstance(color, str):
        if color.startswith('#'):
            if len(color) == 7:
                return parse_hex(color)

            if len(color) == 9:
                return parse_hex(color)

            return

        return pg_color.Color(color)

    return color


__all__ = (
    'TYPE_COLOR',
    'COLOR_ABSOLUTE_RED',
    'COLOR_ABSOLUTE_GREEN',
    'COLOR_ABSOLUTE_BLUE',
    'COLOR_ABSOLUTE_LIGHT_BLUE',
    'COLOR_ABSOLUTE_PINK',
    'COLOR_ABSOLUTE_YELLOW',
    'COLOR_BLACK',
    'COLOR_WHITE',
    'COLOR_RED',
    'COLOR_GREEN',
    'COLOR_BLUE',
    'COLOR_PINK',
    'COLOR_PURPLE',
    'COLOR_DEEP_PURPLE',
    'COLOR_INDIGO',
    'COLOR_LIGHT_BLUE',
    'COLOR_CYAN',
    'COLOR_TEAL',
    'COLOR_LIGHT_GREEN',
    'COLOR_LIME',
    'COLOR_YELLOW',
    'COLOR_AMBER',
    'COLOR_ORANGE',
    'COLOR_DEEP_ORANGE',
    'COLOR_BROWN',
    'COLOR_BLUE_GREY',
    'COLOR_GREY',
    'COLOR_AQUA',
    'COLOR_AQUAMARINE',
    'COLOR_AZURE',
    'COLOR_BEIGE',
    'COLOR_BLUE_VIOLET',
    'COLOR_CADET_BLUE',
    'COLOR_CHOCOLATE',
    'COLOR_CORAL',
    'COLOR_CRIMSON',
    'COLOR_TRANSPARENT',
    'GRADIENT_WITCHING_HOUR',
    'GRADIENT_JSHINE',
    'GRADIENT_WIRETAP',
    'GRADIENT_RASTAFARI',
    'has_alpha',
    'get_alpha',
    'set_alpha',
    'replace_alpha',
    'parse_hex',
    'rgb_to_hex',
    'rgba_to_ahex',
    'argb_to_ahex',
    'hex_to_hexa',
    'ahex_to_hexa',
    'ahex_to_rgba',
    'invert',
    'to_gray',
    'to_black_white',
    'as_ahex',
    'as_rgba',
    'to_readable_color'
)
