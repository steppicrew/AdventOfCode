# https://adventofcode.com/2023/day/01
import math
import re
from itertools import islice
from math import gcd, lcm
from pathlib import Path
from typing import TypeVar

import numpy as np

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

    Stone3d = tuple[tuple[int, int, int], tuple[int, int, int]]

    def parse_line(line: str) -> Stone3d:
        l = re.findall(r'\-?\d+', line)
        return (
            (int(l[0]), int(l[1]), int(l[2])),
            (int(l[3]), int(l[4]), int(l[5]))
        )

    stones3d: tuple[Stone3d, ...] = tuple(
        parse_line(input)
        for input in inputs
    )

    def get_position(t: int, stone: Stone3d) -> tuple[int, int, int]:
        return (
            stone[0][0] + stone[1][0] * t,
            stone[0][1] + stone[1][1] * t,
            stone[0][2] + stone[1][2] * t,
        )

    # find two crossing lines
    # find the common plane
    # find two other lines that cross that plane
    # find a line that crosses those two points

    """
    l1= p1 + s*v1
    l2= p2 + t*v2

    p1 + s*v1 = p2 + t*v2
    s = (p21 + t*v21 - p11) / v11
    p12 + ((p21 + t*v21 - p11) / v11) * v12 = p22 + t*v22
    p12 + p21*v12/v11 + t*v21*v12/v11 - p11*v12/v11 = p22 + t*v22
    t = (p12 + p21*v12/v11 - p11*v12/v11 - p22) / (v22 - v21*v12/v11)

    """

    def test_intersection(s1: Stone3d, s2: Stone3d) -> bool:
        p1, v1 = s1
        p2, v2 = s2

        for _0, _1, _2 in ((0, 1, 2), (1, 2, 0), (2, 0, 1), (0, 2, 1), (1, 0, 2), (2, 1, 0)):
            if v1[_0] == 0:
                continue
            if v2[_1] == v2[_0]*v1[_1]/v1[_0]:
                continue
            t = (p1[_1] + p2[_0]*v1[_1]/v1[_0] - p1[_0]*v1[_1] /
                 v1[_0] - p2[_1]) / (v2[_1] - v2[_0]*v1[_1]/v1[_0])
            s = (p2[_0] + t*v2[_0] - p1[_0]) / v1[_0]
            # debug(s, t)
            return p1[_2] + s * v1[_2] == p2[_2] + t * v2[_2]
        debug("error", s1, s2)
        return False

    def get_parallels() -> list[tuple[Stone3d, Stone3d]]:
        parallels: list[tuple[Stone3d, Stone3d]] = []
        for i1, s1 in enumerate(stones3d):
            for s2 in islice(stones3d, i1 + 1, None):
                lcm0 = lcm(s1[1][0], s2[1][0])
                lcm1 = lcm(s1[1][1], s2[1][1])
                lcm2 = lcm(s1[1][2], s2[1][2])
                max_factor = max(
                    (lcm0 // s1[1][0], lcm1 // s1[1][1], lcm2 // s1[1][2])
                )
                if s1[1][0] * max_factor * s2[1][1] * s2[1][2] == s1[1][1] * max_factor * s2[1][0] * s2[1][2] == s1[1][2] * max_factor * s2[1][0] * s2[1][1]:
                    parallels.append((s1, s2))
        return parallels

    def get_intersects() -> list[tuple[Stone3d, Stone3d]]:
        parallels: list[tuple[Stone3d, Stone3d]] = []
        for i1, s1 in enumerate(stones3d):
            for s2 in islice(stones3d, i1 + 1, None):
                if test_intersection(s1, s2):
                    parallels.append((s1, s2))
        return parallels

    def add(v1: tuple[int, int, int], v2: tuple[int, int, int], factor: int = 1) -> tuple[int, int, int]:
        return (v1[0] + factor * v2[0], v1[1] + factor * v2[1], v1[2] + factor * v2[2])

    def diff(v1: tuple[int, int, int], v2: tuple[int, int, int]) -> tuple[int, int, int]:
        return add(v1, v2, -1)

    def f_add(v1: tuple[float | int, float | int, float | int], v2: tuple[float | int, float | int, float | int], factor: float = 1) -> tuple[float, float, float]:
        return (v1[0] + factor * v2[0], v1[1] + factor * v2[1], v1[2] + factor * v2[2])

    def f_diff(v1: tuple[float, float, float], v2: tuple[float, float, float]) -> tuple[float, float, float]:
        return f_add(v1, v2, -1)

    def dot_prod(v1: tuple[int, int, int], v2: tuple[int, int, int]):
        return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

    def cross_prod(v1: tuple[int, int, int], v2: tuple[int, int, int]):
        return (
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        )

    def _get_plane(p1: tuple[int, int, int], p2: tuple[int, int, int], p3: tuple[int, int, int]) -> tuple[int, int, int, int]:
        '''
        a*p1x + b*p1y + c*p1z + d = 0
        a*p2x + b*p2y + c*p2z + d = 0
        a*p3x + b*p3y + c*p3z + d = 0
        '''
        # These points define two vectors on the plane
        v1 = np.array(p2) - np.array(p1)
        v2 = np.array(p3) - np.array(p1)
        # The cross product of these vectors will give the normal to the plane
        normal = np.cross(v1, v2)
        # The plane equation is Ax + By + Cz + D = 0
        # where A, B, C are the components of the normal, and D can be found by plugging in a point
        D = -np.dot(normal, p1)
        _gcd = gcd(D, *normal)
        return (normal[0] // _gcd, normal[1] // _gcd, normal[2] // _gcd, D // _gcd)

    def get_plane(p1: tuple[int, int, int], p2: tuple[int, int, int], p3: tuple[int, int, int]) -> tuple[int, int, int, int]:
        '''
        a*p1x + b*p1y + c*p1z + d = 0
        a*p2x + b*p2y + c*p2z + d = 0
        a*p3x + b*p3y + c*p3z + d = 0
        '''
        # These points define two vectors on the plane
        v1 = diff(p2, p1)
        v2 = diff(p3, p1)
        # The cross product of these vectors will give the normal to the plane
        normal = cross_prod(v1, v2)
        # The plane equation is Ax + By + Cz + D = 0
        # where A, B, C are the components of the normal, and D can be found by plugging in a point
        d = -dot_prod(normal, p1)
        return (normal[0], normal[1], normal[2], d)
    # debug(get_plane((1, 1, 1), (2, 1, 1), (1, 2, 1)))
    # exit()

    def line_plane_intersection(plane: tuple[int, int, int, int], stone: Stone3d):
        # Unpack the plane parameters
        a, b, c, d = plane

        # a(px + t * vx) + b(py + t * vy) + c(pz + t * vz) + d = 0
        # a*px + a*t*vx + b*py + b*t*vy + c*pz + c*t*vz + d = 0
        # t = -(a*px + b*py + c*pz + d) / (a*vx + b*vy + c*vz)
        # Find the value of t where the line intersects the plane
        # t = -(a*stone[0][0] + b*stone[0][1] + c*stone[0][2] + d) / \
        #     (a*stone[1][0] + b*stone[1][1] + c*stone[1][2])
        _t1 = a*stone[0][0] + b*stone[0][1] + c*stone[0][2] + d
        _t2 = a*stone[1][0] + b*stone[1][1] + c*stone[1][2]
        t = - _t1 // _t2
        if _t1 % _t2 != 0:
            return None
            debug("x", plane, _t1, _t2, t, _t1 % _t2)
        # t = (
        #    - stone[0][0] / (stone[1][0] + b/a*stone[1][1] + c/a*stone[1][2])
        #    - stone[0][1] / (a/b*stone[1][0] + stone[1][1] + c/b*stone[1][2])
        #    - stone[0][2] / (a/c*stone[1][0] + b/c*stone[1][1] + stone[1][2])
        #    - 1 / (a/d*stone[1][0] + b/d*stone[1][1] + c/d*stone[1][2])
        # )
        # Find the intersection point
        return (stone[0][0] + t * stone[1][0], stone[0][1] + t * stone[1][1], stone[0][2] + t * stone[1][2], t)

    def find_closest_point(s1: Stone3d, s2: Stone3d) -> tuple[float, float, float]:
        # Unpack the lines
        p, u = s1
        q, v = s2

        # Compute the direction vector of the shortest line between L1 and L2
        w = diff(p, q)
        a = dot_prod(u, u)
        b = dot_prod(u, v)
        c = dot_prod(v, v)
        d = dot_prod(u, w)
        e = dot_prod(v, w)

        # Compute the parameter for the point on L1 closest to L2
        sc = (b * e - c * d) / (a * c - b ** 2)

        # Compute the point on L1 closest to L2
        return f_add(p, u, sc)

    def find_shortest_dist(s1: Stone3d, s2: Stone3d) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        p0 = find_closest_point(s1, s2)
        p1 = find_closest_point(s2, s1)
        return (p0, f_diff(p0, p1))

    for i1, s1 in enumerate(stones3d):
        for s2 in islice(stones3d, i1 + 1, None):
            plane = get_plane(
                s1[0],
                s2[0],
                diff(s1[0], s1[1])
            )

            p = diff(s2[0], s2[1])
            if p[0] * plane[0] + p[1] * plane[1] + p[2] * plane[2] + plane[3] == 0:
                debug(s1, s2)
                exit()

            # debug(line_plane_intersection(plane, s2))
            # debug(s2)
            # exit()
            # continue

            for s3 in stones3d[:0]:
                if s3 in (s1, s2):
                    continue
                p3 = line_plane_intersection(plane, s3)
                if p3 is None:
                    continue
                debug("plane", plane)
                debug("s1, s2", s1, s2, t)
                debug("p3", p3)
                exit()
                for s4 in stones3d:
                    if s4 in (s1, s2, s3):
                        continue

                    p4 = line_plane_intersection(plane, s4)
                    if p4 is None:
                        continue
                    debug("p4", p4)

                    t_diff = p3[3] - p4[3]

                    p: tuple[float, float, float] = p3[:3]
                    v: tuple[float, float, float] = (
                        (p3[0] - p4[0])/t_diff,
                        (p3[1] - p4[1])/t_diff,
                        (p3[2] - p4[2])/t_diff,
                    )

                    debug(p, v, t_diff)
                    # p0 = diff(p, (v[0] * p3[3], v[1] * p3[3], v[2] * p3[3],))
                    p0 = p[0] - v[0] * p3[3], p[1] - \
                        v[1] * p3[3], p[2] - v[2] * p3[3]

                    debug(p0)
                    debug(sum(p0))
                    exit()

    # 686374601471592: too low

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
