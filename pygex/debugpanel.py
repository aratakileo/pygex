from pygex.color import COLOR_RED, COLOR_WHITE, COLOR_BLACK, COLOR_GREEN, set_alpha
from pygex.core import ver as pygex_ver, get_window, Flippable, MAX_BORDER_RADIUS
from pygex.gui.view import NO_PADDING, VISIBILITY_VISIBLE, VISIBILITY_GONE
from pygex.gui.linearlayout import LinearLayout, ORIENTATION_HORIZONTAL
from pygex.gui.drawable import FadingDrawable
from pygex.gui.drawable import ColorDrawable
from pygame.version import ver as pygame_ver
from pygex.gui.buttonview import ButtonView
from pygex.gui.textview import TextView
from platform import python_version
from pygame.constants import K_F2
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
    def __init__(self, hide=True, is_demonstration_mode=False):
        self.is_showed_button_state_drawable = FadingDrawable.from_color_content(COLOR_RED, MAX_BORDER_RADIUS)
        self.is_hided_button_state_drawable = FadingDrawable.from_color_content(COLOR_GREEN, MAX_BORDER_RADIUS)

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
            gravity=hint.GRAVITY_RIGHT_OF_CENTER | hint.GRAVITY_CENTER_VERTICAL,
            position_offset=(5, 0)
        )

        self.container_linearlayout = LinearLayout(
            (self.debug_textview, self.close_button),
            padding=NO_PADDING,
            orientation=ORIENTATION_HORIZONTAL
        )
        self.is_demonstration_mode = is_demonstration_mode

        self.apply_on_screen()

        if hide:
            self.hide()

    @property
    def is_showing(self):
        return self.debug_textview.visibility == VISIBILITY_VISIBLE

    def apply_on_screen(self):
        window = get_window()

        if window.has_flippable(self):
            window.remove_view(self.container_linearlayout)
            window.remove_flippable(self)
        
        window.add_view(self.container_linearlayout)
        window.add_flippable(self)

    def remove_from_screen(self):
        window = get_window()

        window.remove_view(self.container_linearlayout)
        window.remove_flippable(self)

    def show(self):
        self.debug_textview.visibility = VISIBILITY_VISIBLE

        self.close_button.set_text('X')
        self.close_button.set_background_drawable(self.is_showed_button_state_drawable)
        self.close_button.hint.text = 'Close debug info'

    def hide(self):
        self.debug_textview.visibility = VISIBILITY_GONE

        self.close_button.set_text('O')
        self.close_button.set_background_drawable(self.is_hided_button_state_drawable)
        self.close_button.hint.text = 'Open debug info'
    
    def flip(self):
        window = get_window()
        
        self.debug_textview.set_text(DEBUG_TEXT % (
            pygex_ver,
            pygame_ver,
            python_version(),
            window.fps.__str__() if window.fps_limit is None else f'{window.fps:.3f}/{window.fps_limit}',
            self.is_demonstration_mode.__str__().lower(),
            '\n[f5] - start/stop window record' if self.is_demonstration_mode else ''
        ))

        if self.close_button.is_clicked or window.input.is_up(K_F2):
            if self.is_showing:
                self.hide()
            else:
                self.show()


__all__ = 'DebugPanel',
