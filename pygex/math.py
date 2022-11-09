from typing import Sequence


def interpolate_two_curve_points(point1: Sequence, point2: Sequence, t: float):
    return tuple((1 - t) * point1[i] + t * point2[i] for i in range(2))


def get_curve_point(vertexes: Sequence, r: int, i: int, t: float):
    if r == 0:
        return vertexes[i]

    return interpolate_two_curve_points(
        get_curve_point(vertexes, r - 1, i, t),
        get_curve_point(vertexes, r - 1, i + 1, t),
        t
    )


def get_curve_points(vertexes: Sequence, density=100, fixed_ends=False):
    if len(vertexes) <= 1:
        return []

    if len(vertexes) == 2:
        return *vertexes,

    points = tuple(get_curve_point(vertexes, len(vertexes) - 1, 0, i / density) for i in range(density))

    if fixed_ends:
        if points[0] != vertexes[0]:
            points = vertexes[0], *points

        if points[-1] != vertexes[-1]:
            points = *points, vertexes[-1]

    return points


__all__ = 'interpolate_two_curve_points', 'get_curve_point', 'get_curve_points'
