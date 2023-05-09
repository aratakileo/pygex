from pygex.color import COLOR_RED, COLOR_WHITE, COLOR_BLACK, COLOR_GREEN, set_alpha
from pygex.gui.view import NO_PADDING, VISIBILITY_VISIBLE, VISIBILITY_GONE
from pygex.gui.linearlayout import LinearLayout, ORIENTATION_HORIZONTAL
from pygex.gui.drawable.interactiondrawable import FadingDrawable
from pygex.gui.drawable.drawable import ColorDrawable
from pygame.version import ver as pygame_ver
from pygex.gui.buttonview import ButtonView
from pygex.gui.textview import TextView
from pygex.info import ver as pygex_ver
from pygex.interface import Flippable
from platform import python_version
from pygame.constants import K_F2
from pygex.window import Window
from pygex.gui import hint


DEBUG_TEXT = 'DEBUG INFO:' \
    '\nv%s pygex' \
    '\nv%s pygame' \
    '\nv%s python' \
    '\n%sfps' \
    '\n\nis demonstration mode - %s' \
    '\n\n' \
    '\nSHORTCUTS:' \
    '\n[f1] - take screenshot' \
    '\n[f2] - show/hide this menu%s' \
    '\n[f11] - switch screen mode'


class DebugPanel(Flippable):
    def __init__(self, window: Window, is_demonstration_mode=False, is_visible=True):
        self.is_showed_button_state_drawable = FadingDrawable.from_color_content(COLOR_RED, 90)
        self.is_hided_button_state_drawable = FadingDrawable.from_color_content(COLOR_GREEN, 90)

        self.debug_textview = TextView(
            DEBUG_TEXT,
            text_color=COLOR_WHITE,
            background_drawable_or_color=ColorDrawable(
                set_alpha(COLOR_BLACK, 0xaa),
                border_radius_or_radii=(0,) * 3 + (10,)
            ),
            prerender_during_initialization=False
        )

        self.close_button = ButtonView(
            'X',
            size=(25,) * 2,
            padding=NO_PADDING,
            margin=(5,) * 2 + (0,) * 2,
            background_drawable_or_color=self.is_showed_button_state_drawable,
            prerender_during_initialization=False
        )
        self.close_button.set_hint(
            'Close debug info',
            hint_gravity=hint.GRAVITY_LEFT | hint.GRAVITY_UNDER_CENTER
        )

        self.container_linearlayout = LinearLayout(
            (self.debug_textview, self.close_button),
            padding=NO_PADDING,
            orientation=ORIENTATION_HORIZONTAL
        )
        
        self.window = window
        self.is_demonstration_mode = is_demonstration_mode

        self.apply_on_screen()

        if not is_visible:
            self.hide()

    def apply_on_screen(self):
        self.window.add_view(self.container_linearlayout)
        self.window.add_flip_interface(self)

    def remove_from_screen(self):
        self.window.remove_view(self.container_linearlayout)
        self.window.remove_flip_interface(self)

    def show(self):
        self.container_linearlayout.visibility = VISIBILITY_VISIBLE

    def hide(self):
        self.container_linearlayout.visibility = VISIBILITY_GONE
    
    def flip(self):
        window = self.window
        
        self.debug_textview.set_text(DEBUG_TEXT % (
            pygex_ver,
            pygame_ver,
            python_version(),
            window.fps.__str__() if window.fps_limit is None else f'{window.fps:.3f}/{window.fps_limit}',
            self.is_demonstration_mode.__str__().lower(),
            '\n[f5] - start/stop window record' if self.is_demonstration_mode else ''
        ))

        # self.debug_textview.render_background_surface(True)

        if self.close_button.is_clicked or window.input.is_up(K_F2):
            if self.debug_textview.visibility == VISIBILITY_GONE:
                self.debug_textview.visibility = VISIBILITY_VISIBLE

                self.close_button.set_text('X')
                self.close_button.set_background_drawable(self.is_showed_button_state_drawable)
                self.close_button.set_hint('Close debug info')
            elif self.debug_textview.visibility == VISIBILITY_VISIBLE:
                self.debug_textview.visibility = VISIBILITY_GONE

                self.close_button.set_text('O')
                self.close_button.set_background_drawable(self.is_hided_button_state_drawable)
                self.close_button.set_hint('Open debug info')


__all__ = 'DebugPanel',
