from pygame.surface import SurfaceType


class Flippable:
    def flip(self): ...


class Renderable:
    def render(self, surface: SurfaceType): ...


__all__ = 'Flippable', 'Renderable'
