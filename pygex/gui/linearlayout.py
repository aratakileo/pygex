from pygex.gui.view import View, DEFAULT_PADDING, DEFAULT_SIZE, DEFAULT_POSITION, DEFAULT_GRAVITY, SIZE_WRAP_CONTENT
from pygex.gui.view import GRAVITY_RIGHT, GRAVITY_BOTTOM, GRAVITY_CENTER_HORIZONTAL, GRAVITY_CENTER_VERTICAL
from pygex.gui.view import VISIBILITY_GONE, DEFAULT_MARGIN
from pygex.color import TYPE_COLOR, COLOR_TRANSPARENT
from pygex.gui.drawable.drawable import Drawable
from pygame.surface import SurfaceType
from pygex.image import AlphaSurface
from pygame.event import Event
from typing import Sequence


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
            margin: Sequence[int] = DEFAULT_MARGIN,
            content_gravity: int = DEFAULT_GRAVITY,
            background_drawable_or_color: Drawable | TYPE_COLOR = COLOR_TRANSPARENT,
            prerender_during_initialization: bool = True
    ):
        super().__init__(
            size,
            pos,
            padding,
            margin,
            content_gravity,
            background_drawable_or_color,
            prerender_during_initialization=False
        )

        self._buffered_content_surface: SurfaceType | None = None

        self._orientation = orientation
        self._views: list[View] = [*views]

        self._buffered_views_oriented_total_width = self._buffered_views_oriented_total_height = 0
        self._buffered_views_not_oriented_total_width = self._buffered_views_not_oriented_total_height = 0
        self._buffered_view_sizes = []

        for view in views:
            if view._parent is None:
                view._parent = self
            else:
                self._views.remove(view)
                continue

            view_background_computed_size = view.get_computed_background_size(apply_margin=True, apply_visibility=True)

            self._buffered_view_sizes.append(view_background_computed_size)
            self._buffered_views_oriented_total_width += view_background_computed_size[0]
            self._buffered_views_oriented_total_height += view_background_computed_size[1]
            self._buffered_views_not_oriented_total_width = max(
                self._buffered_views_not_oriented_total_width,
                view_background_computed_size[0]
            )
            self._buffered_views_not_oriented_total_height = max(
                self._buffered_views_not_oriented_total_height,
                view_background_computed_size[1]
            )

        if prerender_during_initialization:
            self.render_content_surface()
            self.render_background_surface()

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, new_value: int):
        old_value = self._orientation
        self._orientation = new_value

        if old_value != new_value:
            self.render_content_surface()

    @property
    def buffered_content_surface(self) -> SurfaceType | None:
        return self._buffered_content_surface

    def rebufferize_not_oriented_view_sizes(self):
        self._buffered_views_not_oriented_total_width = self._buffered_views_not_oriented_total_height = 0

        for buffered_size in self._buffered_view_sizes:
            self._buffered_views_not_oriented_total_width = max(
                self._buffered_views_not_oriented_total_width,
                buffered_size[0]
            )
            self._buffered_views_not_oriented_total_height = max(
                self._buffered_views_not_oriented_total_height,
                buffered_size[1]
            )

    def rebufferize_sizes_for_view(self, view: View):
        # ATTENTION: if you will rename or refactor this method, please do the same to all calling of this method
        # in View and TextView

        if view not in self._views:
            return

        view_index = self._views.index(view)
        view_background_computed_size = view.get_computed_background_size(apply_margin=True, apply_visibility=True)
        buffered_view_background_computed_size = self._buffered_view_sizes[view_index]

        self._buffered_views_oriented_total_width += (
                view_background_computed_size[0]
                -
                buffered_view_background_computed_size[0]
        )
        self._buffered_views_oriented_total_height += (
                view_background_computed_size[1]
                -
                buffered_view_background_computed_size[1]
        )

        self._buffered_view_sizes.insert(view_index, view_background_computed_size)

        del self._buffered_view_sizes[view_index + 1]

        self.rebufferize_not_oriented_view_sizes()

    def add_view(self, view: View):
        if view in self._views or view._parent is not None:
            return

        view._parent = self
        self._views.append(view)

        view_background_computed_size = view.get_computed_background_size(apply_margin=True, apply_visibility=True)

        self._buffered_view_sizes.append(view_background_computed_size)
        self._buffered_views_oriented_total_width += view_background_computed_size[0]
        self._buffered_views_oriented_total_height += view_background_computed_size[1]

        self.rebufferize_not_oriented_view_sizes()

        self.render_content_surface()

    def remove_view(self, view: View):
        if view._parent is not self or view not in self._views:
            return

        view_index = self._views.index(view)
        buffered_view_background_computed_size = self._buffered_view_sizes[view_index]

        self._buffered_views_oriented_total_width -= buffered_view_background_computed_size[0]
        self._buffered_views_oriented_total_height -= buffered_view_background_computed_size[1]

        del self._buffered_view_sizes[view_index], self._views[view_index]

        self.rebufferize_not_oriented_view_sizes()

        self.render_content_surface()

    def get_computed_content_width(self):
        if self._width == SIZE_WRAP_CONTENT:
            if self._orientation == ORIENTATION_HORIZONTAL:
                return self._buffered_views_oriented_total_width

            return self._buffered_views_not_oriented_total_width

        return self.get_computed_background_width() - self.padding_horizontal

    def get_computed_content_height(self):
        if self._height == SIZE_WRAP_CONTENT:
            if self._orientation == ORIENTATION_VERTICAL:
                return self._buffered_views_oriented_total_height

            return self._buffered_views_not_oriented_total_height

        return self.get_computed_background_height() - self.padding_vertical

    def get_computed_background_width(self, apply_margin=False, apply_visibility=False):
        if apply_visibility and self._visibility == VISIBILITY_GONE:
            return 0

        if self._width == SIZE_WRAP_CONTENT:
            return self.get_computed_content_width() + self.padding_horizontal

        return super().get_computed_background_width(apply_margin)

    def get_computed_background_height(self, apply_margin=False, apply_visibility=False):
        if apply_visibility and self._visibility == VISIBILITY_GONE:
            return 0

        if self._height == SIZE_WRAP_CONTENT:
            return self.get_computed_content_height() + self.padding_vertical

        return super().get_computed_background_width(apply_margin)

    def process_event(self, e: Event, offsetted_mouse_x: int, offsetted_mouse_y: int) -> bool:
        if self._visibility == VISIBILITY_GONE or not self.enabled:
            return True

        process_event_for_self = True
        next_children_x_off = next_children_y_off = 0
        computed_content_width, computed_content_height = self.get_computed_content_size()

        if self._orientation == ORIENTATION_HORIZONTAL:
            if self.content_gravity == GRAVITY_RIGHT:
                next_children_x_off += max(computed_content_width - self._buffered_views_oriented_total_width, 0)
            elif self.content_gravity == GRAVITY_CENTER_HORIZONTAL:
                next_children_x_off += max(computed_content_width - self._buffered_views_oriented_total_width, 0) / 2
        else:
            if self.content_gravity == GRAVITY_BOTTOM:
                next_children_y_off += max(computed_content_height - self._buffered_views_oriented_total_height, 0)
            elif self.content_gravity == GRAVITY_CENTER_VERTICAL:
                next_children_y_off += max(computed_content_height - self._buffered_views_oriented_total_height, 0) / 2

        for view, view_size in zip(self._views, self._buffered_view_sizes):
            if self._orientation == ORIENTATION_VERTICAL:
                if self.content_gravity == GRAVITY_RIGHT:
                    next_children_x_off = max(computed_content_width - view_size[0], 0)
                elif self.content_gravity == GRAVITY_CENTER_HORIZONTAL:
                    next_children_x_off = max(computed_content_width - view_size[0], 0) / 2
            else:
                if self.content_gravity == GRAVITY_BOTTOM:
                    next_children_y_off = max(computed_content_height - view_size[1], 0)
                elif self.content_gravity == GRAVITY_CENTER_VERTICAL:
                    next_children_y_off = max(computed_content_height - view_size[1], 0) / 2

            process_event_for_self = view.process_event(
                e,
                offsetted_mouse_x - next_children_x_off,
                offsetted_mouse_y - next_children_y_off
            ) or process_event_for_self

            if view.visibility == VISIBILITY_GONE:
                continue

            if self._orientation == ORIENTATION_HORIZONTAL:
                next_children_x_off += view_size[0]
            else:
                next_children_y_off += view_size[1]

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

        content_width, content_height = self._buffered_content_surface.get_size()
        bg_width = content_width + self.padding_horizontal
        bg_height = content_height + self.padding_vertical

        next_children_x_off = next_children_y_off = 0

        if self._orientation == ORIENTATION_HORIZONTAL:
            if self.content_gravity == GRAVITY_RIGHT:
                next_children_x_off += max(content_width - self._buffered_views_oriented_total_width, 0)
            elif self.content_gravity == GRAVITY_CENTER_HORIZONTAL:
                next_children_x_off += max(content_width - self._buffered_views_oriented_total_width, 0) / 2
        else:
            if self.content_gravity == GRAVITY_BOTTOM:
                next_children_y_off += max(content_height - self._buffered_views_oriented_total_height, 0)
            elif self.content_gravity == GRAVITY_CENTER_VERTICAL:
                next_children_y_off += max(content_height - self._buffered_views_oriented_total_height, 0) / 2

        for view, view_size in zip(self._views, self._buffered_view_sizes):
            if self._orientation == ORIENTATION_VERTICAL:
                if self.content_gravity == GRAVITY_RIGHT:
                    next_children_x_off = max(content_width - view_size[0], 0)
                elif self.content_gravity == GRAVITY_CENTER_HORIZONTAL:
                    next_children_x_off = max(content_width - view_size[0], 0) / 2
            else:
                if self.content_gravity == GRAVITY_BOTTOM:
                    next_children_y_off = max(content_height - view_size[1], 0)
                elif self.content_gravity == GRAVITY_CENTER_VERTICAL:
                    next_children_y_off = max(content_height - view_size[1], 0) / 2

            view.render(self._buffered_content_surface, next_children_x_off, next_children_y_off, (bg_width, bg_height))

            if view.visibility == VISIBILITY_GONE:
                continue

            if self._orientation == ORIENTATION_HORIZONTAL:
                next_children_x_off += view_size[0] + view._margin_right
            else:
                next_children_y_off += view_size[1] + view._margin_bottom


__all__ = 'LinearLayout', 'ORIENTATION_HORIZONTAL', 'ORIENTATION_VERTICAL'
