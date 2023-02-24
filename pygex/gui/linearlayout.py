from pygex.gui.view import View, DEFAULT_PADDING, DEFAULT_SIZE, DEFAULT_POSITION, DEFAULT_GRAVITY, SIZE_WRAP_CONTENT
from pygex.color import TYPE_COLOR, COLOR_TRANSPARENT
from pygex.gui.drawable.drawable import Drawable
from pygex.gui.view import VISIBILITY_GONE
from pygame.surface import SurfaceType
from pygex.image import AlphaSurface
from pygame.event import Event
from typing import Sequence


# TODO: margin support needs to be added


ORIENTATION_HORIZONTAL = 0
ORIENTATION_VERTICAL = 1


class LinearLayout(View):
    def __init__(
            self,
            views: Sequence[View] = (),
            orientation=ORIENTATION_HORIZONTAL,
            size: Sequence[int] = DEFAULT_SIZE,
            pos: Sequence[float | int] = DEFAULT_POSITION,
            padding: Sequence[int] = DEFAULT_PADDING,
            content_gravity: int = DEFAULT_GRAVITY,
            background_drawable_or_color: Drawable | TYPE_COLOR = COLOR_TRANSPARENT,
            prerender_during_initialization: bool = True
    ):
        super().__init__(
            size,
            pos,
            padding,
            content_gravity,
            background_drawable_or_color,
            prerender_during_initialization=False
        )
        self._buffered_oriented_view_steps = []
        self._buffered_content_surface: SurfaceType | None = None
        self._orientation = orientation
        self._views: list[View] = [*views]

        for view in views:
            if view._parent is None:
                view._parent = self
            else:
                self._views.remove(view)

        self.bufferize_oriented_view_steps()

        if prerender_during_initialization:
            self.render_content_surface()
            self.render_background_surface()

    @property
    def buffered_content_surface(self) -> SurfaceType | None:
        return self._buffered_content_surface

    @property
    def orientation(self) -> int:
        return self._orientation

    @orientation.setter
    def orientation(self, value: int):
        old_orientation = self._orientation
        self._orientation = value

        if old_orientation != value:
            self.bufferize_oriented_view_steps()

    def bufferize_oriented_view_steps(self):
        self._buffered_oriented_view_steps = [
            (
                view.get_computed_background_width() if self._orientation == ORIENTATION_HORIZONTAL
                else view.get_computed_background_height()
            ) for view in self._views
        ]

    def add_view(self, view: View):
        if view in self._views or view._parent is not None:
            return

        view._parent = self
        self._views.append(view)

        self.bufferize_oriented_view_steps()
        self.render_content_surface()

    def remove_view(self, view: View):
        if view._parent is not self or view not in self._views:
            return

        view_index = self._views.index(view)
        del self._buffered_oriented_view_steps[view_index], self._views[view_index]

        self.render_content_surface()

    def get_computed_content_width(self):
        if self._width == SIZE_WRAP_CONTENT:
            calculated_width = 0

            if self._orientation == ORIENTATION_HORIZONTAL:
                for view in self._views:
                    calculated_width += view.get_computed_background_width()
            else:
                for view in self._views:
                    calculated_width = max(calculated_width, view.get_computed_background_width())

            return calculated_width

        return self.get_computed_background_width() - self.padding_horizontal

    def get_computed_content_height(self):
        if self._height == SIZE_WRAP_CONTENT:
            calculated_height = 0

            if self._orientation == ORIENTATION_VERTICAL:
                for view in self._views:
                    calculated_height += view.get_computed_background_height()
            else:
                for view in self._views:
                    calculated_height = max(calculated_height, view.get_computed_background_height())

            return calculated_height

        return self.get_computed_background_height() - self.padding_vertical

    def get_computed_background_width(self):
        if self._width == SIZE_WRAP_CONTENT:
            return self.get_computed_content_width() + self.padding_horizontal

        return super().get_computed_background_width()

    def get_computed_background_height(self):
        if self._height == SIZE_WRAP_CONTENT:
            return self.get_computed_content_height() + self.padding_vertical

        return super().get_computed_background_width()

    def process_event(self, e: Event, offsetted_mouse_x: int, offsetted_mouse_y: int) -> bool:
        if self.visibility == VISIBILITY_GONE or not self.enabled:
            return True

        next_children_x_off = next_children_y_off = 0
        process_event_for_self = True

        for view, step in zip(self._views, self._buffered_oriented_view_steps):
            process_event_for_self = view.process_event(
                e,
                offsetted_mouse_x - next_children_x_off,
                offsetted_mouse_y - next_children_y_off
            ) or process_event_for_self

            if self._orientation == ORIENTATION_HORIZONTAL:
                next_children_x_off += step
            else:
                next_children_y_off += step

        if process_event_for_self:
            return super().process_event(e, offsetted_mouse_x, offsetted_mouse_y)

        return True

    def flip(self):
        for view in self._views:
            view.flip()

        super().flip()

    def render_content_surface(self):
        if not self._views:
            self._buffered_content_surface = None
            return

        self._buffered_content_surface = AlphaSurface(self.get_computed_content_size())
        next_children_x_off = next_children_y_off = 0

        width, height = self._buffered_content_surface.get_size()
        width += self.padding_horizontal
        height += self.padding_vertical

        for view, step in zip(self._views, self._buffered_oriented_view_steps):
            view.render(self._buffered_content_surface, next_children_x_off, next_children_y_off, (width, height))

            if self._orientation == ORIENTATION_HORIZONTAL:
                next_children_x_off += step
            else:
                next_children_y_off += step


__all__ = 'LinearLayout', 'ORIENTATION_HORIZONTAL', 'ORIENTATION_VERTICAL'
