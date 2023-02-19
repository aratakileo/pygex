from pygex.text import ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, ALIGN_BLOCK, DEFAULT_FONT_SIZE, TextRenderer
from pygex.gui.view import View, SIZE_WRAP_CONTENT, DEFAULT_PADDING, GRAVITY_LEFT, GRAVITY_TOP
from pygex.gui.drawable.drawable import Drawable
from pygex.color import COLOR_TYPE, C_BLACK
from pygame.surface import SurfaceType
from pygame.font import FontType
from typing import Sequence


class TextView(View):
    def __init__(
            self,
            text: str,
            text_color: COLOR_TYPE = C_BLACK,
            size: Sequence[int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
            pos: Sequence[float | int] = (0, 0),
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity=GRAVITY_LEFT | GRAVITY_TOP,
            text_align=ALIGN_LEFT,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | COLOR_TYPE = ...,
            font_antialiasing=True,
            render_content_during_initialization=True
    ):
        super().__init__(
            size,
            pos,
            padding,
            content_gravity,
            background_drawable_or_color,

            # ATTENTION: If True, the Surface content is rendered here before all the attributes of the class
            # are initialized, which is why the crash occurs
            render_content_during_initialization=False
        )

        self.text_renderer = TextRenderer(
            text,
            text_color,
            self.get_computed_content_size(),
            font_or_font_size,
            text_align,
            text_line_spacing,
            text_lines_number,
            text_paragraph_space,
            font_antialiasing
        )

        if render_content_during_initialization:
            self.render_content_surface()

    @property
    def buffered_content_surface(self) -> SurfaceType | None:
        return self.text_renderer.text_surface

    def render_content_surface(self):
        self.text_renderer.set_size(self.get_computed_content_size())


__all__ = 'ALIGN_LEFT', 'ALIGN_RIGHT', 'ALIGN_CENTER', 'ALIGN_BLOCK', 'TextView',
