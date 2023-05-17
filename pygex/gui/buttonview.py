from pygex.gui.view import DEFAULT_SIZE, DEFAULT_PADDING, DEFAULT_POSITION, GRAVITY_CENTER, DEFAULT_MARGIN
from pygex.color import TYPE_COLOR, COLOR_WHITE, COLOR_GREEN
from pygex.font import DEFAULT_FONT_SIZE, TYPE_FONT
from pygex.gui.drawable import FadingDrawable
from pygex.gui.drawable import Drawable
from pygex.gui.textview import TextView
from pygex.text import ALIGN_CENTER
from typing import Sequence


class ButtonView(TextView):
    def __init__(
            self,
            text: str,
            text_color: TYPE_COLOR = COLOR_WHITE,
            size: Sequence[int] = DEFAULT_SIZE,
            pos: Sequence[float | int] = DEFAULT_POSITION,
            padding: Sequence[int] = DEFAULT_PADDING,
            margin: Sequence[int] = DEFAULT_MARGIN,
            content_gravity=GRAVITY_CENTER,
            text_align=ALIGN_CENTER,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: TYPE_FONT = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | TYPE_COLOR = COLOR_GREEN,
            font_antialiasing=True,
            prerender_during_initialization=True
    ):
        if not isinstance(background_drawable_or_color, Drawable):
            background_drawable_or_color = FadingDrawable.from_color_content(background_drawable_or_color, 10)

        super().__init__(
            text,
            text_color,
            size,
            pos,
            padding,
            margin,
            content_gravity,
            text_align,
            text_line_spacing,
            text_lines_number,
            text_paragraph_space,
            font_or_font_size,
            background_drawable_or_color,
            font_antialiasing,
            prerender_during_initialization
        )

    def set_background_drawable(self, drawable_or_color: Drawable | TYPE_COLOR):
        if not isinstance(drawable_or_color, Drawable):
            drawable_or_color = FadingDrawable.from_color_content(drawable_or_color, 10)

        super().set_background_drawable(drawable_or_color)


__all__ = 'ButtonView'
