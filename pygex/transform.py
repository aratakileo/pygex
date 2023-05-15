from pygame.image import frombuffer as pg_image_frombuffer, tostring as pg_image_tostring
from pygame.draw import rect as pg_draw_rect, ellipse as pg_draw_ellipse
from pygame.transform import smoothscale as pg_smoothscale
from pygex.color import COLOR_BLACK, COLOR_WHITE
from pygame.surface import Surface, SurfaceType
from pygex.color import TYPE_COLOR, as_rgba
from pygame.constants import SRCALPHA
from typing import Sequence


try:
    from PIL import Image as PillowImage, ImageFilter as PillowImageFilter

    def pillow_to_pygame(source_surface: PillowImage):
        return pg_image_frombuffer(source_surface.tobytes(), source_surface.size, 'RGBA')


    def pygame_to_pillow(source_surface: SurfaceType):
        return PillowImage.frombytes('RGBA', source_surface.get_size(), pg_image_tostring(source_surface, 'RGBA'))


    def fast_gaussian_blur(source_surface: SurfaceType, radius: int):
        """
        Fast gaussian blur [faster than `pygame-ce`.transform.gaussian_blur(...)]
        :param source_surface: source Surface
        :param radius: blur radius
        """
        return pillow_to_pygame(pygame_to_pillow(source_surface).filter(PillowImageFilter.GaussianBlur(radius)))
except ImportError:
    pass


def cutout_by_mask(source_surface: SurfaceType, mask: SurfaceType):
    """
    The cutout color on the mask is black (#ff000000 or (0, 0, 0, 255))
    :param source_surface: source Surface
    :param mask: mask for cutout
    """
    new_source = source_surface.copy()

    for x in range(0, source_surface.get_size()[0]):
        for y in range(0, source_surface.get_size()[1]):
            if mask.get_at((x, y)) == (0, 0, 0, 255):
                new_source.set_at((x, y), 0x00000000)

    return new_source


def round_corners(
        source_surface: SurfaceType,
        border_top_left_radius: int,
        border_top_right_radius: int,
        border_bottom_left_radius: int,
        border_bottom_right_radius: int
):
    mask_surface = Surface(source_surface.get_size())
    mask_surface.fill(COLOR_BLACK)

    if -1 in (border_top_left_radius, border_top_right_radius, border_bottom_left_radius, border_bottom_right_radius):
        pg_draw_ellipse(mask_surface, COLOR_WHITE, mask_surface.get_rect())
    else:
        pg_draw_rect(
            mask_surface,
            COLOR_WHITE,
            mask_surface.get_rect(),
            0,
            -1,
            border_top_left_radius,
            border_top_right_radius,
            border_bottom_left_radius,
            border_bottom_right_radius
        )

    return cutout_by_mask(source_surface, mask_surface)


def gradient(size: Sequence[int], colors: Sequence[TYPE_COLOR], is_vertical=False):
    colors_line_surface = Surface((1, len(colors)) if is_vertical else (len(colors), 1), SRCALPHA, 32)

    for i in range(len(colors)):
        colors_line_surface.set_at((0, i) if is_vertical else (i, 0), as_rgba(colors[i]))

    return pg_smoothscale(colors_line_surface, size)


__all__ = (
    'pillow_to_pygame',
    'pygame_to_pillow',
    'fast_gaussian_blur',
    'cutout_by_mask',
    'round_corners',
    'gradient'
)
