from pygex.gui.view import View, DEFAULT_SIZE, DEFAULT_PADDING, DEFAULT_POSITION, DEFAULT_GRAVITY, DEFAULT_MARGIN
from pygex.text import ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, ALIGN_BLOCK, TextRenderer
from pygex.color import TYPE_COLOR, COLOR_BLACK, COLOR_TRANSPARENT
from pygex.font import TYPE_FONT, DEFAULT_FONT_SIZE
from pygex.gui.drawable import Drawable
from pygex.surface import TYPE_SURFACE
from typing import Sequence


class TextView(View):
    def __init__(
            self,
            text: str,
            text_color: TYPE_COLOR = COLOR_BLACK,
            size: Sequence[int] = DEFAULT_SIZE,
            pos: Sequence[float | int] = DEFAULT_POSITION,
            padding: Sequence[int] = DEFAULT_PADDING,
            margin: Sequence[int] = DEFAULT_MARGIN,
            content_gravity=DEFAULT_GRAVITY,
            text_align=ALIGN_LEFT,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: TYPE_FONT = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | TYPE_COLOR = COLOR_TRANSPARENT,
            font_antialiasing=True,
            prerender_during_initialization=True
    ):
        super().__init__(
            size,
            pos,
            padding,
            margin,
            content_gravity,
            background_drawable_or_color,

            # ATTENTION: if True, the Surface content is rendered here before all the attributes of the class
            # are initialized, which is why the crash occurs
            prerender_during_initialization=False
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

        if prerender_during_initialization:
            self.render_content_surface()
            self.render_background_surface()

    @property
    def text(self):
        return self.text_renderer._text

    def set_text(self, text: str):
        old_size = (-1, -1) if self.text_renderer.text_surface is None else self.text_renderer.text_surface.get_size()

        if not self.text_renderer.set_text(text):
            return

        if (
                self.text_renderer.text_surface is None or old_size != self.text_renderer.text_surface.get_size()
        ) and 'rebufferize_sizes_for_view' in self._parent.__dir__():
            self._parent.rebufferize_sizes_for_view(self)

        if isinstance(self._parent, View):
            self._parent.render_content_surface()

        self.render_background_surface()

    @property
    def buffered_content_surface(self) -> TYPE_SURFACE | None:
        return self.text_renderer.text_surface

    def render_content_surface(self):
        self.text_renderer.set_size(self.get_computed_content_size())

        if isinstance(self._parent, View):
            self._parent.render_content_surface()


__all__ = 'ALIGN_LEFT', 'ALIGN_RIGHT', 'ALIGN_CENTER', 'ALIGN_BLOCK', 'TextView',
