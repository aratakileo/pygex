from pygame.constants import SRCALPHA
from pygame.surface import Surface
from typing import Sequence


def AlphaSurface(size: Sequence[int], flags: int = 0):
    return Surface(size, flags | SRCALPHA, 32)


__all__ = 'AlphaSurface',
