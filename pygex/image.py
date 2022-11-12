from pygame.image import frombuffer as pg_image_frombuffer, tostring as pg_image_tostring
from PIL import Image as PillowImage, ImageFilter as PillowImageFilter
from pygame.surface import Surface, SurfaceType
from pygame.draw import rect as pg_draw_rect
from typing import Sequence


def pillow_to_pygame(source: PillowImage):
    return pg_image_frombuffer(source.tobytes(), source.size, 'RGBA')


def pygame_to_pillow(source: SurfaceType):
    return PillowImage.frombytes('RGBA', source.get_size(), pg_image_tostring(source, 'RGBA'))


def blur(source: SurfaceType, radius: int):
    return pillow_to_pygame(pygame_to_pillow(source).filter(PillowImageFilter.GaussianBlur(radius)))


def cutout_by_mask(source: SurfaceType, mask: SurfaceType):
    """
    The cutout color on the mask is black (#000000)

    :param source: original Surface

    :param mask: mask for cutout
    """
    new_source = source.copy()

    for x in range(0, source.get_size()[0]):
        for y in range(0, source.get_size()[1]):
            if mask.get_at((x, y)) == (0, 0, 0, 255):
                new_source.set_at((x, y), 0x00000000)

    return new_source


def round_corners(source: SurfaceType, radius: int | tuple[int, int, int, int] | Sequence):
    """
    Rounding the borders of image (Surface)

    :param source: source image
    :param radius: value by which the corners will be rounded: `radius` or `top_left, top_right, bottom_left, bottom_tight`
    """
    radius = (radius,) if isinstance(radius, int) else (-1, *radius)
    mask = Surface(source.get_size())
    mask.fill(0x000000)

    pg_draw_rect(mask, 0xffffff, (0, 0, *source.get_size()), 0, *radius)

    return cutout_by_mask(source, mask)


__all__ = 'pillow_to_pygame', 'pygame_to_pillow', 'blur', 'cutout_by_mask', 'round_corners'
