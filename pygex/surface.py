from pygame.surface import Surface, SurfaceType
from pygame.constants import SRCALPHA
from typing import Sequence


TYPE_SURFACE = SurfaceType


def AlphaSurface(size: Sequence[int], flags: int = 0):
    return Surface(size, flags | SRCALPHA, 32)


__all__ = 'AlphaSurface', 'TYPE_SURFACE'
