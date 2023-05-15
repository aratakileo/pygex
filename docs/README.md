# Pygex docs

### Install

To install `pygex` just use this command
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

### Quick start

Welcome to `pygex`! Once you've got [`pygex` installed](#install), the next question is how to get a game loop running. `Pygex`, unlike `pygame-ce`, does not just give you full control over the execution of the program, however, it does not limit you in this. You just need to tell the library what exactly you want to gain control over, and what functionality offered by the library you want to give up. These limitations mean that you don't have to deal with low-level stuff, for the full operation of your game, it will be enough for you to write a few lines of code.

It is important to understand that `pygex` cannot replace `pygame-ce`, it is only an additional convenient tool for working with `pygame-ce`.

Here is a good example of a basic setup (initializes and opens the window, updates the screen)

```py
import pygex

# initializing the window
window = pygex.Window(
    size=(1280, 720),
    title='My first game with pygex!',
    fps_limit=60,
    resizable=True
)
window.bg_color = pygex.color.COLOR_WHITE  # setting the color that will erase everything that remains of the last frame

while window.is_running:
    # DESCRIBE YOUR GAME'S RENDERING CODE HERE

    # the flip() method is needed to display your work on the screen, as well as for Window to handle various events 
    # and internal logic
    window.flip()
```
[[Take a look at a `pygame-ce` version of the example]](https://pyga.me/docs/#:~:text=%23%20Example%20file%20showing%20a%20basic%20pygame%20%22game%20loop%22)

Here is a slightly more fleshed out example, which shows you how to move something (a circle in this case) around on screen
```py
import pygame
import pygex

# initializing the window
window = pygex.Window(
    size=(1280, 720),
    title='My first game with pygex!',
    fps_limit=60,
    resizable=True
)
window.bg_color = pygex.color.COLOR_WHITE  # setting the color that will erase everything that remains of the last frame
player_pos = pygame.Vector2(window.surface.get_rect().center)
player_speed = 300

while window.is_running:
    pygame.draw.circle(window.surface, pygex.color.COLOR_DEEP_PURPLE, player_pos, 40)

    if window.input.is_applying(pygame.K_w):
        player_pos.y -= player_speed * window.dt

    if window.input.is_applying(pygame.K_s):
        player_pos.y += player_speed * window.dt

    if window.input.is_applying(pygame.K_a):
        player_pos.x -= player_speed * window.dt

    if window.input.is_applying(pygame.K_d):
        player_pos.x += player_speed * window.dt

    # the flip() method is needed to display your work on the screen, as well as for Window to handle various events
    # and internal logic
    window.flip()
```
[[Take a look at a `pygame-ce` version of the example]](https://pyga.me/docs/#:~:text=%23%20Example%20file%20showing%20a%20circle%20moving%20on%20screen)

Here is another example, which shows you how to use `pygex.gui` on screen
```py
import pygex

# initializing the window
window = pygex.Window(
    size=(1280, 720),
    title='My first game with pygex!',
    fps_limit=60,
    resizable=True,
)
window.bg_color = pygex.color.COLOR_WHITE  # setting the color that will erase everything that remains of the last frame

helloworld_drawable = pygex.gui.drawable.GradientDrawable(
    pygex.color.GRADIENT_WITCHING_HOUR[::-1],
    is_vertical=True,
    border_radius_or_radii=30
)
helloworld_textview = pygex.gui.TextView(
    'Hello World!',
    text_color=pygex.color.COLOR_WHITE,
    size=(pygex.gui.SIZE_MATCH_PARENT,) * 2,
    margin=(10,) * 4,
    content_gravity=pygex.gui.GRAVITY_CENTER,
    font_or_font_size=500,
    background_drawable_or_color=helloworld_drawable
)

window.add_view(helloworld_textview)

while window.is_running:
    window.render_views()  # render all views

    # the flip() method is needed to display your work on the screen, as well as for Window to handle various events
    # and internal logic
    window.flip()
```

Result of the code execution:
![](preview-1.png)

For more in depth reference, check out [`pygame-ce` docs](https://pyga.me/docs/), or reference the API documentation by module section below.

### References
- [pygex.Window](window.md)
