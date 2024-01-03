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
    Stone3dNorm = tuple[Coord, Coord, Coord_f, int]

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

    def norm(v: Coord) -> Coord_f:
        norm = sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
        return (v[0] / norm, v[1] / norm, v[2] / norm)

    def v_abs_sqr(v: Coord) -> int:
        return sum(_ * _ for _ in v)

    stones3d_norm: tuple[Stone3dNorm, ...] = tuple(
        (*stone, norm(stone[1]), v_abs_sqr(stone[1]))
        for stone in stones3d
    )

    def line_parametric(p: Coord, direction: Coord, t: int) -> Coord:
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

    def v_abs(v: Coord_f) -> float:
        return sqrt(sum(_ * _ for _ in v))

    def dot_prod(v1: Coord, v2: Coord) -> int:
        return sum(c[0] * c[1] for c in zip(v1, v2))

    def dot_prod_f(v1: Coord_f, v2: Coord_f) -> float:
        return sum(c[0] * c[1] for c in zip(v1, v2))

    def diff(p1: Coord, p2: Coord) -> Coord:
        return (
            p1[0] - p2[0],
            p1[1] - p2[1],
            p1[2] - p2[2],
        )

    def step1():

        parallelities: dict[tuple[Stone3dNorm, Stone3dNorm], float] = {}

        def get_parallelity(s1: Stone3dNorm, s2: Stone3dNorm) -> float:
            if (s1, s2) not in parallelities:
                # parallelities[(s1, s2)] = v_abs(cross_prod_f(s1[2], s2[2]))
                parallelities[(s1, s2)] = abs(dot_prod_f(s1[2], s2[2]))
            return parallelities[(s1, s2)]

        s1, s2, s3, *_ = stones3d_norm
        min_tuple: tuple[int, int, int] = (0, 1, 2)
        min_parallelity: float = get_parallelity(
            s1, s2) + get_parallelity(s1, s3) + get_parallelity(s2, s3)
        max_tuple: tuple[int, int, int] = (0, 1, 2)
        max_parallelity = min_parallelity
        for i1, s1 in enumerate(stones3d_norm):
            for i2, s2 in enumerate(islice(stones3d_norm, i1 + 1, None)):
                p12 = get_parallelity(s1, s2)
                for i3, s3 in enumerate(islice(stones3d_norm, i1 + i2 + 2, None)):
                    p = p12 + get_parallelity(s1, s3) + get_parallelity(s2, s3)
                    if p < min_parallelity:
                        min_parallelity = p
                        min_tuple = (i1, i1 + i2 + 1, i1 + i2 + i3 + 2)
                    if p > max_parallelity:
                        max_parallelity = p
                        max_tuple = (i1, i1 + i2 + 1, i1 + i2 + i3 + 2)

        print("min", min_parallelity, min_tuple)
        print("max", max_parallelity, max_tuple)
        min_s1, min_s2, min_s3 = (
            stones3d_norm[min_tuple[0]],
            stones3d_norm[min_tuple[1]],
            stones3d_norm[min_tuple[2]],
        )
        max_s1, max_s2, max_s3 = (
            stones3d_norm[max_tuple[0]],
            stones3d_norm[max_tuple[1]],
            stones3d_norm[max_tuple[2]],
        )
        print("dot12", dot_prod_f(min_s1[2], min_s2[2]), dot_prod(
            min_s1[1], min_s2[1]))
        print("dot13", dot_prod_f(min_s1[2], min_s3[2]), dot_prod(
            min_s1[1], min_s3[1]))
        print("dot23", dot_prod_f(min_s2[2], min_s3[2]), dot_prod(
            min_s2[1], min_s3[1]))
        return min_tuple

    def step2(i1: int, i2: int, i3: int):
        def v_abs_sqr(v: Coord) -> int:
            return sum(c * c for c in v)

        def test(p: Coord, v: Coord, s: Stone3dNorm) -> int | None:
            dividend = s[0][1] * v[0] - p[1] * \
                v[0] - v[1] * s[0][0] + v[1] * p[0]
            divisor = v[1] * s[1][0] - s[1][1] * v[0]
            if dividend % divisor != 0:
                return None
            u = dividend // divisor
            if u < 0:
                return None

            dividend = s[0][0] + u * s[1][0] - p[0]
            divisor = v[0]
            if dividend % divisor != 0:
                return None
            t = dividend // divisor

            if p[2] + t * v[2] == s[0][2] + u * s[1][2]:
                return t

            return None

        s1, s2, s3 = sorted(
            (stones3d_norm[i1], stones3d_norm[i2], stones3d_norm[i3]),
            key=lambda s: v_abs_sqr(s[1]),
            reverse=True
        )
        for t1 in range(10_000):
            if t1 % 100 == 0:
                print(t1)
            s1_t1 = line_parametric(s1[0], s1[1], t1)
            for t2 in range(10_000):
                s2_t2 = line_parametric(s2[0], s2[1], t2)
                v12: Coord = diff(s1_t1, s2_t2)
                v_gcd = gcd(*v12)
                if v_gcd > 1:
                    v12 = (v12[0] // v_gcd, v12[1] // v_gcd, v12[2] // v_gcd)

                t3 = test(s1_t1, v12, s3)
                if t3 is not None:
                    print("Found solution", t1, t2)

        print(s1, s2, s3)
        exit()

    # print(step1())
    # exit()
    # min: 40, 177, 271 (1: 0, 3, 4)
    # max: 109, 202, 288
    if REF == 1:
        print(step2(0, 3, 4))
    elif REF == 0:
        print(step2(40, 177, 271))

    exit()

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
