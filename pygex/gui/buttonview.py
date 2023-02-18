from pygex.gui.view import SIZE_WRAP_CONTENT, DEFAULT_PADDING, GRAVITY_CENTER_HORIZONTAL, GRAVITY_CENTER_VERTICAL
from pygex.gui.drawable.interactiondrawable import InteractionDrawable, IS_NO_INTERACTION, IS_IN_INTERACTION
from pygame.constants import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, WINDOWLEAVE
from pygex.gui.drawable.interactiondrawable import IS_END_OF_INTERACTION
from pygex.gui.drawable.drawable import Drawable, ColorDrawable
from pygex.gui.view import VISIBILITY_VISIBLE, VISIBILITY_GONE
from pygame.display import get_window_size as pg_win_get_size
from pygex.text import ALIGN_CENTER, DEFAULT_FONT_SIZE
from pygex.color import COLOR_TYPE, C_WHITE, C_GREEN
from pygame.mouse import get_pos as pg_mouse_get_pos
from pygex.gui.textview import TextView
from pygame.surface import SurfaceType
from pygame.font import FontType
from pygex.gui.hint import Hint
from pygame.event import Event
from pygame.rect import Rect
from typing import Sequence


class ButtonView(TextView):
    def __init__(
            self,
            text: str = 'Click Me!',
            text_color: COLOR_TYPE = C_WHITE,
            size: Sequence[int] = (SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT),
            pos: Sequence[float | int] = (0, 0),
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity=GRAVITY_CENTER_HORIZONTAL | GRAVITY_CENTER_VERTICAL,
            text_align=ALIGN_CENTER,
            text_line_spacing: float | int = 0,
            text_lines_number: int = ...,
            text_paragraph_space: float | int = 0,
            font_or_font_size: FontType | int = DEFAULT_FONT_SIZE,
            background_drawable_or_color: Drawable | InteractionDrawable | COLOR_TYPE = InteractionDrawable(
                ColorDrawable(C_GREEN, 10)
            ),
            font_antialiasing=True,
            render_content_during_initialization=True
    ):
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

        self._hint: Hint | None = None
        self._hint_offset = 3
        self._hint_anchor_is_mouse = False

        self._background_drawable_is_interaction_drawable = isinstance(self._background_drawable, InteractionDrawable)
        self._interaction_status = IS_NO_INTERACTION
        self._is_focused = False

    @property
    def is_clicked(self):
        return self._interaction_status == IS_END_OF_INTERACTION

    @property
    def is_focused(self):
        return self._is_focused

    def get_interaction_rect(self):
        return Rect(
            self.x,
            self.y,
            self.get_background_width(),
            self.get_background_height(),
        )

    def set_hint(
            self,
            text: str,
            offset=3,
            anchor_is_mouse=False,
            hint_gravity: int = Hint.GRAVITY_CENTER_HORIZONTAL | Hint.GRAVITY_UNDER_CENTER
    ):
        self._hint_offset = offset
        self._hint_anchor_is_mouse = anchor_is_mouse

        if self._hint is None:
            self._hint = Hint(text, gravity=hint_gravity)

            return

        self._hint.text = text
        self._hint.gravity = hint_gravity

    def process_event(self, e: Event):
        if self.visibility == VISIBILITY_GONE:
            return

        if e.type == WINDOWLEAVE:
            # ATTENTION: This is necessary so that the focus is removed from the View when the mouse goes outside
            # the window, while the View is at the window border, which is why the mouse coordinates are not updated
            # and the events associated with it are no longer read
            self._is_focused = False

        interaction_status_is_changed = False

        if e.type == MOUSEMOTION:
            self._is_focused = self.get_interaction_rect().collidepoint(pg_mouse_get_pos())
        elif e.type == MOUSEBUTTONDOWN and self._is_focused:
            self._interaction_status = IS_IN_INTERACTION
            interaction_status_is_changed = True
        elif e.type == MOUSEBUTTONUP and self._interaction_status == IS_IN_INTERACTION:
            self._interaction_status = IS_END_OF_INTERACTION if self._is_focused else IS_NO_INTERACTION
            interaction_status_is_changed = True

        if interaction_status_is_changed and self._background_drawable_is_interaction_drawable:
            self._background_drawable.set_interaction_status(self._interaction_status)

            if self._interaction_status == IS_IN_INTERACTION:
                self._background_surface_buffer = self._background_drawable.render(self.get_background_size())

    def flip(self):
        # ATTENTION: if the View like a ButtonView will be added to the Window view list,
        # then this method will call earlier than the render method

        if self.visibility == VISIBILITY_GONE:
            self._interaction_status = IS_NO_INTERACTION
            self._is_focused = False

            if self._background_drawable_is_interaction_drawable \
                    and self._background_drawable._interaction_status != IS_NO_INTERACTION:
                self._background_drawable.set_interaction_status(IS_NO_INTERACTION, animate=False)
                self._background_surface_buffer = self._background_drawable.render(self.get_background_size())

            return

        if self._interaction_status == IS_END_OF_INTERACTION:
            self._interaction_status = IS_NO_INTERACTION

            if self._background_drawable_is_interaction_drawable:
                self._background_drawable.set_interaction_status(self._interaction_status)

        if self._background_drawable_is_interaction_drawable:
            self._background_drawable.flip()

    def set_background_drawable(self, drawable_or_color: Drawable | InteractionDrawable | COLOR_TYPE):
        super().set_background_drawable(drawable_or_color)

        self._background_drawable_is_interaction_drawable = isinstance(self._background_drawable, InteractionDrawable)

    def render(self, surface: SurfaceType):
        if self.visibility != VISIBILITY_VISIBLE:
            return

        if self._background_drawable_is_interaction_drawable and self._background_drawable.is_need_to_be_rendered():
            self._background_surface_buffer = self._background_drawable.render(self.get_background_size())

        super().render(surface)

        if self._is_focused and self._hint is not None:
            hint_pos_or_rect = (*pg_mouse_get_pos(), 25, 25) if self._hint_anchor_is_mouse else (
                self.x + (self.get_background_width() / 2),
                self.y + self.get_background_height() + self._hint_offset
            )

            self._hint.render(
                surface,
                hint_pos_or_rect,
                (0, 0, *pg_win_get_size())
            )


__all__ = 'ButtonView',
