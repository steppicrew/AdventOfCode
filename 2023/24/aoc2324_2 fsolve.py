# https://adventofcode.com/2023/day/01
import math
import re
from decimal import Decimal
from fractions import Fraction
from itertools import islice
from math import gcd, lcm, sqrt
from pathlib import Path
from typing import Any, TypeVar

import numpy as np
from scipy.optimize import anderson, broyden2, fsolve

REF = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part: str = "_" + part_match[1] if part_match else ""

EXT = "_ref" + str(REF) + ".txt" if REF else ".txt"
path = Path(__file__).parent.absolute()
with open(file=path/("input" + EXT), mode="r", encoding='utf-8') as file:
    inputs: list[str] = file.read().rstrip().split("\n")
# ---


def print_off(*args):  # pylint: disable=unused-argument
    pass


debug = print
debug_off = print_off


def run() -> int:
    result: int = 0

    Coord = tuple[int, int, int]
    Coord_f = tuple[float, float, float]
    Stone3d = tuple[Coord, Coord]

    def parse_line(line: str) -> Stone3d:
        l = re.findall(r'\-?\d+', line)
        return (
            (int(l[0]), int(l[1]), int(l[2])),
            (int(l[3]), int(l[4]), int(l[5])),
        )

    stones3d: tuple[Stone3d, ...] = tuple(
        parse_line(input)
        for input in inputs
    )

    def line_parametric(p: Coord, direction: Coord, t: float) -> Coord_f:
        return (p[0] + t * direction[0], p[1] + t * direction[1], p[2] + t * direction[2])

    def cross_prod(v1: Coord, v2: Coord) -> Coord:
        return (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        )

    def cross_prod_f(v1: Coord_f, v2: Coord_f) -> Coord_f:
        return (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        )

    def dot_prod(v1: Coord, v2: Coord) -> int:
        return sum(c[0] * c[1] for c in zip(v1, v2))

    def norm(v: Coord_f) -> Coord_f:
        norm = sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
        return (v[0] / norm, v[1] / norm, v[2] / norm)

    def get_closest_points(s1: Stone3d, s2: Stone3d) -> tuple[Coord_f, Coord_f]:
        p1, v1 = s1
        p2, v2 = s2
        v3 = cross_prod(v1, v2)
        a = np.array([
            [-v1[0], v2[0], -v3[0]],
            [-v1[1], v2[1], -v3[1]],
            [-v1[2], v2[2], -v3[2]],
        ], np.longlong)
        b = np.array(
            [p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]],
            np.longlong
        )
        x = np.linalg.solve(a, b)
        s, t, u = x[0], x[1], x[2]

        return (
            (p1[0] + s * v1[0], p1[1] + s * v1[1], p1[2] + s * v1[2]),
            (p2[0] + t * v2[0], p2[1] + t * v2[1], p2[2] + t * v2[2]),
        )

    def get_plane_intersection(plane1: tuple[Coord_f, Coord_f], plane2: tuple[Coord_f, Coord_f]) -> tuple[Coord_f, Coord_f]:
        v1_norm = norm(plane1[1])
        v2_norm = norm(plane2[1])
        v = cross_prod_f(v1_norm, v2_norm)

    def add(p1: Coord_f, p2: Coord_f, t: float = 1) -> Coord_f:
        return (
            p1[0] + t * p2[0],
            p1[1] + t * p2[1],
            p1[2] + t * p2[2],
        )

    def diff(p1: Coord, p2: Coord) -> Coord:
        return (
            p1[0] - p2[0],
            p1[1] - p2[1],
            p1[2] - p2[2],
        )

    def diff_f(p1: Coord_f, p2: Coord_f) -> Coord_f:
        return add(p1, p2, -1)

    # Example usage
    L1 = stones3d[0]
    L2 = stones3d[1]
    L3 = stones3d[2]

    m1, m2 = get_closest_points(L1, L2)
    plane_1 = (m1, add(m2, m1, -1))
    plane_2 = (m2, add(m1, m2, -1))
    plane_q = (m2, cross_prod_f(L2[1], add(L3[0], m2, -1)))

    def intersection_equations(t, P1, d1, P2, d2, P3, d3):
        # Points on each line for a given t
        p1 = line_parametric(P1, d1, t[0])
        p2 = line_parametric(P2, d2, t[1])
        p3 = line_parametric(P3, d3, t[2])

        v1 = diff_f(p1, p2)
        v2 = diff_f(p1, p3)
        factor = 1000

        return cross_prod_f(
            (v1[0] * factor, v1[1] * factor, v1[2] * factor),
            (v2[0] * factor, v2[1] * factor, v2[2] * factor),
        )

    def vector_abs_sqr(v: Coord_f) -> float:
        debug(v, Fraction(v[0]) * Fraction(v[0]) + Fraction(v[1]) * Fraction(v[1]) + Fraction(v[2]) * Fraction(v[2]),
              Fraction(v[0]) * Fraction(v[0]), Fraction(v[1]) * Fraction(v[1]), Fraction(v[2]) * Fraction(v[2]))
        return sum((c * c) for c in v)

    def find_intersecting_line(*lines: Stone3d):

        def intersection_equations(t):
            # Points on each line for a given t
            print("t", t, tuple(zip(lines, t)))
            points = tuple(
                tuple(
                    c[0] + v[1] * c[1]
                    for c in zip(*v[0])
                )
                for v in zip(lines, t)
            )

            vectors = tuple(
                diff_f(p, points[(i + 1) % len(points)]) for i, p in enumerate(points))

            cross_products = tuple(cross_prod_f(
                vector, vectors[(i+1) % len(vectors)]) for i, vector in enumerate(vectors))

            return tuple(vector_abs_sqr(cp) for cp in cross_products)

        # Initial guess for the fsolve function
        initial_guess = [1 for _ in lines]

        # Solve for t values
        t_solution = fsolve(intersection_equations,
                            initial_guess)
        debug("1", t_solution)

        debug(intersection_equations(t_solution))

        return t_solution

    result2 = find_intersecting_line(*stones3d[:5])
    debug(result2)
    exit()

    # L1 = stones3d[3]
    # L2 = stones3d[4]
    # L3 = stones3d[5]

    get_closest_points(L1, L2)

    t1, t2, t3 = find_intersecting_line(L1, L2, L3)
    print(t1, t2, t3)

    # L1 = stones3d[3]
    L2 = stones3d[4]
    L3 = stones3d[5]
    t1, t2, t3 = find_intersecting_line(L1, L2, L3)
    print(t1, t2, t3)
    exit()

    P1 = (
        L1[0][0] + int(t1) * L1[1][0],
        L1[0][1] + int(t1) * L1[1][1],
        L1[0][2] + int(t1) * L1[1][2],
    )
    P2 = (
        L2[0][0] + int(t2) * L2[1][0],
        L2[0][1] + int(t2) * L2[1][1],
        L2[0][2] + int(t2) * L2[1][2],
    )
    P3 = (
        L3[0][0] + int(t3) * L3[1][0],
        L3[0][1] + int(t3) * L3[1][1],
        L3[0][2] + int(t3) * L3[1][2],
    )

    v4 = (
        (P1[0] - P2[0]) / (int(t1) - int(t2)),
        (P1[1] - P2[1]) / (int(t1) - int(t2)),
        (P1[2] - P2[2]) / (int(t1) - int(t2)),
    )
    debug(v4)
    debug(P1, P2, P3)

    # 686374601471592: too low

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
