from pygex.surface import TYPE_SURFACE


class Flippable:
    def flip(self): ...


DEFAULT_RENDER_LAYER_FOR_RENDER_OVER_GUI = 1000
DEFAULT_RENDER_LAYER_FOR_RENDER_UNDER_GUI = -1000


class Renderable:
    # ATTENTION: render layer system is not support for child views
    render_layer = 0

    def render(self, surface: TYPE_SURFACE): ...


__all__ = (
    'Flippable',
    'Renderable',
    'DEFAULT_RENDER_LAYER_FOR_RENDER_OVER_GUI',
    'DEFAULT_RENDER_LAYER_FOR_RENDER_UNDER_GUI'
)
