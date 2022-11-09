from pygame import color as pg_color
from typing import Sequence

colorValue = pg_color.Color | int | str | Sequence


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


def from_ahex(color: str):
    if color.startswith('#'):
        color = color[1:]

    return int(color[:2], 16), *from_hex(color[2:])


def from_hexa(color: str):
    if color.startswith('#'):
        color = color[1:]

    return from_hex(color[:6]), int(color[6:], 16)


def rgb_to_hex(color: Sequence | pg_color.Color):
    return (color[0] & 0xff) << 16 | (color[1] & 0xff) << 8 | (color[2] & 0xff)


def rgba_to_ahex(color: Sequence | pg_color.Color):
    return (color[3] & 0xff) << 24 | rgb_to_hex(color)


def argb_to_ahex(color: Sequence | pg_color.Color):
    return (color[0] & 0xff) << 24 | rgb_to_hex(color[1:])


def hex_to_hexa(color: int, alpha: int = 0xff):
    return color << 8 | alpha


def ahex_to_hexa(color: int):
    return remove_alpha(color) << 8 | get_alpha(color)


def color_as_int(color: colorValue):
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
                    return from_hex(color)

                if len(color) == 9:
                    return from_ahex(color)

                return None

            color = pg_color.Color(color)

    if isinstance(color, pg_color.Color):
        return rgba_to_ahex(color)

    return color


def invert(color: colorValue, invert_alpha=False):
    color = color_as_int(color)

    if color is None:
        return None

    alpha = get_alpha(color)

    if invert_alpha:
        alpha = ~alpha & 0xff

    return set_alpha(~remove_alpha(color) & 0xffffff, alpha)


def to_gray(color: colorValue):
    color = color_as_int(color)

    if color is None:
        return None

    segment = (((color >> 16) & 0xff) * 299 + ((color >> 8) & 0xff) * 587 + (color & 0xff) * 114) // 1000

    return rgba_to_ahex((segment, segment, segment, get_alpha(color)))


def to_black_white(color: colorValue):
    color = color_as_int(color)

    if color is None:
        return None

    segment = to_gray(color) & 0xff
    segment = 0x00 if segment < 0x7f else 0xff

    return rgba_to_ahex((segment, segment, segment, get_alpha(color)))


def to_pygame_alpha_color(color: colorValue):
    """
    Converting color from AHEX or HEX to HEXA (color format in pygame is HEXA)

    :param color: alpha format: AHEX, HEX, RGBA
    """
    if isinstance(color, int):
        if has_alpha(color):
            return ahex_to_hexa(color)

        return hex_to_hexa(color)

    if isinstance(color, Sequence) and len(color) < 4:
        return *color, 255  # converting rgb to rgba

    if isinstance(color, str):
        if color.startswith('#'):
            if len(color) == 7:
                return from_hex(color)

            if len(color) == 9:
                return from_ahex(color)

            return None

        return pg_color.Color(color)

    return color


def get_optimal_text_color(background_color: colorValue):
    background_color = color_as_int(background_color)

    if background_color is None:
        return None

    return to_black_white(invert(background_color))


__all__ = (
    'colorValue',
    'has_alpha',
    'get_alpha',
    'set_alpha',
    'from_hex',
    'from_ahex',
    'from_hexa',
    'rgb_to_hex',
    'rgba_to_ahex',
    'argb_to_ahex',
    'hex_to_hexa',
    'ahex_to_hexa',
    'color_as_int',
    'invert',
    'to_gray',
    'to_black_white',
    'to_pygame_alpha_color',
    'get_optimal_text_color'
)
