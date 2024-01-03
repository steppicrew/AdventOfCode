# https://adventofcode.com/2023/day/01
import re
from math import sqrt
from pathlib import Path
from typing import TypeVar

from scipy.optimize import fsolve

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


T = TypeVar("T", int, float)


def run() -> int:
    result: int = 0

    Coord = tuple[int, int, int]
    Coord_f = tuple[float, float, float]
    Stone3d = tuple[Coord, Coord]

    class Stone:
        def __init__(self, stone: Stone3d) -> None:
            self.stone = stone
            self.p, self.v = stone
            self._norm: Coord_f | None = None
            self._abs_square: int | None = None

        def pos(self, t: T) -> tuple[T, T, T]:
            return (
                self.p[0] + t * self.v[0],
                self.p[1] + t * self.v[1],
                self.p[2] + t * self.v[2],
            )

        @property
        def norm(self) -> Coord_f:
            if self._norm is None:
                norm = sqrt(self.abs_sqr)
                self._norm = (self.v[0] / norm,
                              self.v[1] / norm, self.v[2] / norm)
            return self._norm

        @property
        def abs_sqr(self) -> int:
            if self._abs_square is None:
                self._abs_square = (
                    self.v[0] * self.v[0]
                    + self.v[1] * self.v[1]
                    + self.v[2] * self.v[2]
                )
                assert self._abs_square > 0
            return self._abs_square

        def __str__(self):
            return self.stone.__str__()

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

    stones: tuple[Stone, ...] = tuple(
        Stone(stone)
        for stone in stones3d
    )

    """
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


    def dot_prod(v1: tuple[T, T, T], v2: tuple[T, T, T]) -> T:
        return sum(#type:ignore
            c[0] * c[1] for c in zip(v1, v2)
            )

    def neg(v: tuple[T, T, T]) -> tuple[T, T, T]:
        return (  # type:ignore
            -v[0],
            -v[1],
            -v[2],
        )

    """

    def diff(p1: tuple[T, T, T], p2: tuple[T, T, T]) -> tuple[T, T, T]:
        return (
            p1[0] - p2[0],
            p1[1] - p2[1],
            p1[2] - p2[2],
        )

    def mult(v: Coord | Coord_f, t: float) -> Coord_f:
        return (
            t*v[0],
            t*v[1],
            t*v[2],
        )

    def add(*vectors: tuple[T, T, T]) -> tuple[T, T, T]:
        return (  # type:ignore
            sum(v[0] for v in vectors),
            sum(v[1] for v in vectors),
            sum(v[2] for v in vectors),
        )

    def solve(s1: Stone, s2: Stone, s3: Stone, s4: Stone, initial_guess: list[float]) -> list[float]:
        F_Type = tuple[
            float, float, float,
            float, float, float,
            float, float, float,
        ]

        def f(x: F_Type) -> F_Type:
            vx, vy, vz, r, s, t1, t2, t3, t4 = x
            v = vx, vy, vz

            p = s1.pos(t1)
            return (
                *diff(s2.pos(t2), add(p, v)),
                *diff(s3.pos(t3), add(p, mult(v, r))),
                *diff(s4.pos(t4), add(p, mult(v, s))),
            )

        # initial_guess = [*p20mp10, 0, 0, t10, t20, t30, t40]
        result = fsolve(f, initial_guess, full_output=True, xtol=1e-15)
        solution: list[float] = result[0]
        print("ier", result[2], result[3])
        print("info", result[1])
        print(solution)
        vx, vy, vz, r, s, t1, t2, t3, t4 = solution
        print("v", vx, vy, vz)
        print("t1-4", t1, t2, t3, t4)
        p0 = add(s1.p, mult(s1.v, t1))
        # v = diff(s2.pos(t2), p0)
        v = (vx, vy, vz)
        print("P0 + v", add(p0, v))
        print("P2 + t2*v2", s2.pos(t2))
        print("P0 + r*v", add(p0, mult(v, r)))
        print("P3 + t3*v3", s3.pos(t3))
        print("P0 + s*v", add(p0, mult(v, s)))
        print("P4 + t4*v4", s4.pos(t4))
        return solution

    test_stones = stones[0], stones[40], stones[177], stones[271]

    base_length = 2_000_000_000_000

    t10 = base_length/4
    t20 = base_length/3
    t30 = base_length/3
    t40 = base_length/2

    p20mp10 = diff(test_stones[1].pos(t10), test_stones[0].pos(t20))

    solution = solve(*test_stones, [*p20mp10, 0, 0, t10, t20, t30, t40])

    vx, vy, vz, _r, _s, t1, t2, _t3, _t4 = solution

    def test_solution(vector: Coord, s1: Stone, t1: int, s2: Stone, t2: int) -> Stone | None:
        p1 = s1.pos(t1)
        p2 = s2.pos(t2)
        p2mp1 = diff(p2, p1)  # pylint: disable=arguments-out-of-order
        if p2mp1 != vector:
            return None
        dt = t2 - t1
        real_vector_f = mult(vector, 1/dt)
        real_vector = (
            int(real_vector_f[0]),
            int(real_vector_f[1]),
            int(real_vector_f[2]),
        )
        real_p0_float = diff(p1, mult(real_vector, t1))
        real_p0 = (
            int(real_p0_float[0]),
            int(real_p0_float[1]),
            int(real_p0_float[2]),
        )
        return Stone((real_p0, real_vector))

    my_stone = test_solution(
        (int(vx), int(vy), int(vz)),
        test_stones[0], int(t1),
        test_stones[1], int(t2)
    )
    if my_stone is not None:
        result = sum(my_stone.p)

    # solution = solve(*s, solution)
    # 686374601471592: too low

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
