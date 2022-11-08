from pygame.image import frombuffer as pg_image_frombuffer, tostring as pg_image_tostring
from PIL import Image as PillowImage, ImageFilter as PillowImageFilter
from pygame.surface import Surface, SurfaceType
from pygame.draw import rect as pg_draw_rect
from pygame import pg_SRCALPHA
from typing import Sequence


def pillow_to_pygame_image(img: PillowImage):
    return pg_image_frombuffer(img.tobytes(), img.size, 'RGBA')


def pygame_to_pillow_image(img: SurfaceType):
    return PillowImage.frombytes('RGBA', img.get_size(), pg_image_tostring(img, 'RGBA'))


def set_blur(img: SurfaceType, radius: int):
    return pillow_to_pygame_image(pygame_to_pillow_image(img).filter(PillowImageFilter.GaussianBlur(radius)))


def set_round_corners(img: SurfaceType, radius: int | tuple[int, int, int, int] | Sequence):
    """
    Rounding the borders of image (Surface)

    :param img: source image
    :param radius: value by which the corners will be rounded: `radius` or `top_left, top_right, bottom_left, bottom_tight`
    """
    radius = (radius,) if isinstance(radius, int) else (-1, *radius)
    size = img.get_size()
    mask = Surface(size)
    mask.fill(0x000000)

    pg_draw_rect(mask, 0xffffff, (0, 0, *size), 0, *radius)

    new_img = Surface(size, img.get_flags() | pg_SRCALPHA, 32)

    for x in range(0, img.get_size()[0]):
        for y in range(0, img.get_size()[1]):
            if mask.get_at((x, y)) == (255, 255, 255, 255):
                new_img.set_at((x, y), img.get_at((x, y)))

    return new_img


__all__ = 'pillow_to_pygame_image', 'pygame_to_pillow_image', 'set_blur', 'set_round_corners'
