# https://adventofcode.com/2023/day/01
import re
from fractions import Fraction
from itertools import islice
from math import gcd, sqrt
from pathlib import Path

from matplotlib import pyplot as plt

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

    class Stone:
        def __init__(self, stone: Stone3d) -> None:
            self.stone = stone
            self.p, self.v = stone
            self._norm: Coord_f | None = None
            self._abs_square: int | None = None

        def pos(self, t: int) -> Coord:
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

    """

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

    # fig, ax = plt.subplots()
    ax = plt.axes(projection='3d')
    default_length = 2_000_000_000_000
    for stone, t1, t2 in (
        (stones[40], default_length//3, default_length//2),  # blue
        (stones[177], default_length//3, default_length),  # orange
        (stones[271], default_length//2, default_length//3*2),  # green
        (stones[0], default_length//4, default_length//3)  # red
    ):

        start = stone.pos(t1)
        end = stone.pos(t2)
        # ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]])
        ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]])
        ax.scatter(start[0], start[1], start[2], s=10)
    plt.show()

    exit()

    # 686374601471592: too low

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
