from pygame.font import FontType, get_init, init, Font
from pygex.resource import RESOURCES_PATH


def __get_font_resource_path(font_resource_name: str):
    return RESOURCES_PATH + 'font/' + font_resource_name


TYPE_FONT = FontType | int

FONT_FIRA_CODE_BOLD = __get_font_resource_path('FiraCode-Bold.ttf')
FONT_FIRA_CODE_REGULAR = __get_font_resource_path('FiraCode-Regular.ttf')
FONT_FIRA_MONO_BOLD_ITALIC = __get_font_resource_path('FiraMono-BoldItalic.ttf')
FONT_FIRA_MONO_REGULAR_ITALIC = __get_font_resource_path('FiraMono-RegularItalic.ttf')
FONT_NOTO_SANS_JP_BOLD = __get_font_resource_path('NotoSansJP-Bold.otf')
FONT_NOTO_SANS_JP_REGULAR = __get_font_resource_path('NotoSansJP-Regular.otf')
FONT_NOTO_SANS_SC_BOLD = __get_font_resource_path('NotoSansSC-Bold.otf')
FONT_NOTO_SANS_SC_REGULAR = __get_font_resource_path('NotoSansSC-Regular.otf')

DEFAULT_FONT_NAME = FONT_FIRA_CODE_REGULAR
DEFAULT_FONT_SIZE = 15

_font_buffer = {}


def get_pygame_font(font_or_font_size: FontType | int = DEFAULT_FONT_SIZE):
    if not get_init():
        init()

    if isinstance(font_or_font_size, int):
        font_or_font_size = max(font_or_font_size, 1)

        if font_or_font_size not in _font_buffer:
            _font_buffer[font_or_font_size] = Font(DEFAULT_FONT_NAME, font_or_font_size)

        return _font_buffer[font_or_font_size]

    return font_or_font_size


__all__ = (
    'TYPE_FONT',
    'FONT_FIRA_CODE_BOLD',
    'FONT_FIRA_CODE_REGULAR',
    'FONT_FIRA_MONO_REGULAR_ITALIC',
    'FONT_FIRA_MONO_BOLD_ITALIC',
    'FONT_NOTO_SANS_JP_BOLD',
    'FONT_NOTO_SANS_JP_REGULAR',
    'FONT_NOTO_SANS_SC_BOLD',
    'FONT_NOTO_SANS_SC_REGULAR',
    'DEFAULT_FONT_NAME',
    'DEFAULT_FONT_SIZE',
    'get_pygame_font',
)
