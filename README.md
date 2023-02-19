# PygEx (Pygame Extended)
Extended library for pygame users

##### Navigation
- [Preview](#preview)
- [Requirements](#requirements)
- [How to install `pygex`](#how-to-install-pygex)

### Preview

![](https://github.com/TeaCondemns/pygex/releases/download/v0.3/preview.gif)

[[Run this demo project]](https://github.com/teacondemns/pygex/releases/tag/v0.3)

Current development version: `0.3.1` (the same version will be [installed](#how-to-install-pygex))

Use examples:
- [Drawing application](https://github.com/teacondemns/vector-paint)
- [Bezier curve editor](https://github.com/teacondemns/bezier-curve)

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

[[Look for previous version]](https://github.com/teacondemns/pygex/releases/tag/v0.3)

[[Look for other versions]](https://github.com/teacondemns/pygex/releases)
