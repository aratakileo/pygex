from typing import Sequence


def generate_curve(
        vertexes: Sequence[Sequence[float | int]],
        density: int, fixed_ends=False
) -> tuple | tuple[Sequence[float | int]]:
    """
    Fast Bézier curve generator
    :param vertexes: the vertexes on the basis of which the curve will be generated
    :param density: the number of segments that the curve will consist of
    :param fixed_ends: if true, then the beginning and end of the curve will be the same where it was at the specified
    vertices
    """

    if len(vertexes) <= 2:
        return *vertexes,

    points = ()

    for i in range(density):
        t = i / density
        prepoints = *vertexes,

        while len(prepoints) > 1:
            new_prepoints = ()

            for k in range(len(prepoints) - 1):
                new_prepoints = *new_prepoints, tuple(
                    prepoints[k][j] * (1 - t) + prepoints[k + 1][j] * t for j in range(2)
                )

            prepoints = new_prepoints

        points = *points, *prepoints

    if fixed_ends:
        if points[0] != vertexes[0]:
            points = vertexes[0], *points

        if points[-1] != vertexes[-1]:
            points = *points, vertexes[-1]

    return points


__all__ = 'generate_curve',
