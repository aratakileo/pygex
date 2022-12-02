# PygEx (Pygame Extended)
Extended library for pygame users

##### Navigation
- [Preview](#preview)
- [Requirements](#requirements)
- [How to install](#how-to-install-pygex)

### Preview
Use examples:
- [Drawing application](https://github.com/teacondemns/upaint)
- [Bezier curve editor](https://github.com/teacondemns/bezier-curve)

This module include:
- More advanced mouse controller (`mouse.py`: each button can be in one of four pressing statuses: not pressed, button down, held, button up)
- More advanced keys input controller (`input.py`: each key can be in one of four pressing statuses: not pressed, key down, held, key up)
- Extensive functionality for manipulating color (by default, all color values of this module are accepted as an argument of functions that are not included in the submodule `color.py `, are expected only in HEX or AHEX format, and not as in pygame - HEXA)
- Function for calculating the Bezier curve (`math.py`)
- Functions for Gaussian blur, mask cutting, taking screenshot, and corner rounding for pygame Surface (`image.py`)
- Function for more convenient text rendering, with the ability to buffer the font by size, as well as render text by font size (`text.py`)
- Drawing the simplest interface elements (`draw.py`)
- Convenient interface for creating and managing a window (`window.py`)

### Requirements
- `python >= 3.10`
- `pygame >= 2.0`

### How to install `pygex`
Just use this command
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
