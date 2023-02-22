from pygex.gui.view import DEFAULT_SIZE, DEFAULT_PADDING, DEFAULT_POSITION, GRAVITY_CENTER_HORIZONTAL
from pygex.color import TYPE_COLOR, COLOR_WHITE, COLOR_GREEN, to_readable_color, replace_alpha
from pygex.gui.drawable.interactiondrawable import FadingDrawable
from pygex.gui.drawable.drawable import Drawable, ColorDrawable
from pygex.text import ALIGN_CENTER, DEFAULT_FONT_SIZE
from pygex.gui.view import GRAVITY_CENTER_VERTICAL
from pygex.gui.textview import TextView
from pygame.font import FontType
from typing import Sequence


class ButtonView(TextView):
    def __init__(
            self,
            text: str,
            text_color: TYPE_COLOR = COLOR_WHITE,
            size: Sequence[int] = DEFAULT_SIZE,
            pos: Sequence[float | int] = DEFAULT_POSITION,
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity=GRAVITY_CENTER_HORIZONTAL | GRAVITY_CENTER_VERTICAL,
            text_align=ALIGN_CENTER,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | TYPE_COLOR = COLOR_GREEN,
            font_antialiasing=True,
            render_content_during_initialization=True
    ):
        if not isinstance(background_drawable_or_color, Drawable):
            background_drawable_or_color = FadingDrawable(
                ColorDrawable(background_drawable_or_color, 10),
                effect_color=replace_alpha(to_readable_color(background_drawable_or_color), 0x96)
            )

        super().__init__(
            text,
            text_color,
            size,
            pos,
            padding,
            content_gravity,
            text_align,
            text_line_spacing,
            text_lines_number,
            text_paragraph_space,
            font_or_font_size,
            background_drawable_or_color,
            font_antialiasing,
            render_content_during_initialization
        )

    def set_background_drawable(self, drawable_or_color: Drawable | TYPE_COLOR):
        if not isinstance(drawable_or_color, Drawable):
            drawable_or_color = FadingDrawable(
                ColorDrawable(drawable_or_color, 10),
                effect_color=replace_alpha(to_readable_color(drawable_or_color), 0x96)
            )

        super().set_background_drawable(drawable_or_color)
