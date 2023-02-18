# PygEx (Pygame Extended)
Extended library for pygame users

##### Navigation
- [Preview](#preview)
- [Requirements](#requirements)
- [How to install `pygex`](#how-to-install-pygex)

### Preview
Current development version: `0.3` (the same version will be [installed](#how-to-install-pygex))

Use examples:
- [Drawing application](https://github.com/teacondemns/vector-paint)
- [Bezier curve editor](https://github.com/teacondemns/bezier-curve)

Demo project:
![image](https://user-images.githubusercontent.com/83653555/219899773-66055e2a-9379-4c72-b6ee-60dbd70f56f9.png)
```py
from pygex.info import pygex_ver
import pygame
import pygex


window = pygex.Window()
window.bg_color = 0xffffff
window.fps_limit = 120

fullscreen_toast = pygex.Toast('To exit full screen press [F11]')

some_textview = pygex.gui.TextView(
    'Um... Excuse me? What you actually doing in my house? Please leave now!',
    size=(pygex.gui.SIZE_MATCH_PARENT, pygex.gui.SIZE_MATCH_PARENT),
    text_line_spacing=-2,
    text_align=pygex.gui.ALIGN_CENTER,
    content_gravity=pygex.gui.GRAVITY_CENTER_HORIZONTAL | pygex.gui.GRAVITY_CENTER_VERTICAL,
    text_color=0xcaf0f8,
    font_or_font_size=50,
    background_drawable_or_color=pygex.gui.drawable.GradientDrawable(
        (0xcaf0f8, 0x00b4d8, 0xcaf0f8),
        border_width=10,
        border_color=0xcaf0f8,
        is_vertical=True
    )
)
some_textview.render_content_surface()

debug_text = '=========DEBUG MENU=========' \
    '\n - pygex: v%s' \
    '\n - %s/%ifps' \
    '\n\n' \
    '\n=========SHORTCUTS==========' \
    '\n - press [f1] to take screenshot' \
    '\n - press [f2] to show/hide this menu' \
    '\n - press [f11] to switch screen mode'

debug_textview = pygex.gui.TextView(
    '',
    text_color=pygex.color.C_WHITE,
    background_drawable_or_color=pygex.gui.drawable.ColorDrawable(
        0xaa000000,
        border_radius_or_radii=(0, 0, 0, 10)
    )
)


debug_button = pygex.gui.ButtonView('[!]', pos=(5, 5), render_content_during_initialization=False)
debug_button.get_background_drawable().get_content().set_border_radius(90)
debug_button.get_background_drawable().get_content().color = pygex.color.C_RED | 0xaa000000
debug_button.set_hint(
    'Close debug menu',
    hint_gravity=pygex.gui.Hint.GRAVITY_LEFT | pygex.gui.Hint.GRAVITY_UNDER_CENTER
)


def open_or_close_debug_menu():
    if debug_textview.visibility == pygex.gui.VISIBILITY_GONE:
        debug_textview.visibility = pygex.gui.VISIBILITY_VISIBLE
        debug_button.set_hint('Close debug menu')
    elif debug_textview.visibility == pygex.gui.VISIBILITY_VISIBLE:
        debug_textview.visibility = pygex.gui.VISIBILITY_GONE
        debug_button.set_hint('Open debug menu')
        debug_button.x = 5


window.add_view(some_textview)
window.add_view(debug_textview)
window.add_view(debug_button)


while True:
    debug_textview.set_text(debug_text % (pygex_ver, f'{window.fps:.3f}', window.fps_limit))

    if debug_button.x == 5 and debug_textview.visibility == pygex.gui.VISIBILITY_VISIBLE:
        debug_button.x += debug_textview.get_background_width()

    if debug_button.is_clicked:
        open_or_close_debug_menu()

    if window.input.is_up(pygame.K_F1):
        window.take_screenshot()
    elif window.input.is_up(pygame.K_F2):
        open_or_close_debug_menu()
    elif window.input.is_up(pygame.K_F11):
        window.fullscreen = not window.fullscreen

        if window.fullscreen:
            fullscreen_toast.show()
        else:
            fullscreen_toast.cancel()

    window.flip()

```

<!--
This module include:
- More advanced mouse controller (`mouse.py`: each button can be in one of four pressing statuses: not pressed, button down, held, button up)
- More advanced keys input controller (`input.py`: each key can be in one of five pressing statuses: not pressed, key down, held, key up; key up or key hold for first 0.5s and after that 0.1s)
- Extensive functionality for manipulating color (by default, all color values of this module are accepted as an argument of functions that are not included in the submodule color.py, are expected only in HEX or AHEX format, and not as in pygame - HEXA, but accepted in RGBA format as and in pygame)
- Function for calculating the Bézier curve (`math.py`)
- Functions for Gaussian blur, mask cutting, generate gradient Surface, and corner rounding for pygame Surface (`image.py`)
- Function for more convenient text rendering, with the ability to buffer the font by size, as well as render text by font size both unaligned in any way, and aligned with extensive settings (`text.py`: `pygex.text.render_aligned_text(...)` - also include `align` `=` `pygex.text.ALIGN_LEFT` or `pygex.text.ALIGN_RIGHT` or `pygex.text.ALIGN_CENTER` or `pygex.text.ALIGN_BLOCK`, `line_spacing`, `line_number`, `paragraph_space`, `size` `=` `(..., ...)` or `(SIZE_WRAP_CONTENT, ...)` or `(..., SIZE_WRAP_CONTENT)` or `(SIZE_WRAP_CONTENT, SIZE_WRAP_CONTENT)`)
- Drawing the simplest grid (`draw.py`)
- Convenient interface for creating and managing a window (`window.py`: taking screenshots, showing toasts, better full screen mode toggle system, `pygex.mouse` and `pygex.input` are also integrated into this interface)
- Interface for toasts (short text messages) displaying (`gui/toast.py`)
- Interface for text hints displaying (`gui/hint.py`)
-->

### Requirements
- `python >= 3.10`
- `pygame >= 2.0.1`

### How to install `pygex`
To install `pygex` of [current version](#preview) just use this command
```
pip install git+https://github.com/teacondemns/pygex.git
```

<details>
  <summary>for <code>windows</code></summary>
  

```
py -m pip install git+https://github.com/teacondemns/pygex.git
```
</details>

<details>
  <summary>for <code>unix</code>/<code>macos</code></summary>
  

```
python3 -m pip install git+https://github.com/teacondemns/pygex.git
```
</details>

If `pygame` installation failed for `python3.11`, just use this command to fix it
```
pip install pygame --pre
```

<details>
  <summary>for <code>windows</code></summary>
  

```
py -m pip install pygame --pre
```
</details>

<details>
  <summary>for <code>unix</code>/<code>macos</code></summary>
  

```
python3 -m pip install pygame --pre
```
</details>

[[Look for previous version]](https://github.com/teacondemns/pygex/releases/tag/v0.2.dev3)

[[Look for other versions]](https://github.com/teacondemns/pygex/releases)
