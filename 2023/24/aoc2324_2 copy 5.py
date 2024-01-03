# https://adventofcode.com/2023/day/01
import re
from fractions import Fraction
from itertools import islice
from math import gcd, sqrt
from pathlib import Path

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

    if True:
        """
        Find tree most orthogonal stones and try to find a solution
        """
        def step1():
            """
            Find three most (and least) parallel lines
            """

            parallelities: dict[tuple[Stone3d, Stone3d], float] = {}

            def get_parallelity(s1: Stone, s2: Stone) -> float:
                _s1, _s2 = s1.stone, s2.stone
                if (_s1, _s2) not in parallelities:
                    # parallelities[(s1, s2)] = v_abs(cross_prod_f(s1[2], s2[2]))
                    parallelities[(_s1, _s2)] = abs(
                        dot_prod_f(s1.norm, s2.norm))
                return parallelities[(_s1, _s2)]

            s1, s2, s3, *_ = stones
            min_tuple: tuple[int, int, int] = (0, 1, 2)
            min_parallelity: float = get_parallelity(
                s1, s2) + get_parallelity(s1, s3) + get_parallelity(s2, s3)
            max_tuple: tuple[int, int, int] = (0, 1, 2)
            max_parallelity = min_parallelity
            for i1, s1 in enumerate(stones):
                for i2, s2 in enumerate(islice(stones, i1 + 1, None)):
                    p12 = get_parallelity(s1, s2)
                    for i3, s3 in enumerate(islice(stones, i1 + i2 + 2, None)):
                        p = p12 + \
                            get_parallelity(s1, s3) + get_parallelity(s2, s3)
                        if p < min_parallelity:
                            min_parallelity = p
                            min_tuple = (i1, i1 + i2 + 1, i1 + i2 + i3 + 2)
                        if p > max_parallelity:
                            max_parallelity = p
                            max_tuple = (i1, i1 + i2 + 1, i1 + i2 + i3 + 2)

            print("min", min_parallelity, min_tuple)
            print("max", max_parallelity, max_tuple)
            min_s1, min_s2, min_s3 = (
                stones[min_tuple[0]],
                stones[min_tuple[1]],
                stones[min_tuple[2]],
            )
            max_s1, max_s2, max_s3 = (
                stones[max_tuple[0]],
                stones[max_tuple[1]],
                stones[max_tuple[2]],
            )
            print(
                "dot12",
                dot_prod_f(min_s1.norm, min_s2.norm),
                dot_prod(min_s1.v, min_s2.v)
            )
            print(
                "dot13",
                dot_prod_f(min_s1.norm, min_s3.norm),
                dot_prod(min_s1.v, min_s3.v)
            )
            print(
                "dot23",
                dot_prod_f(min_s2.norm, min_s3.norm),
                dot_prod(min_s2.v, min_s3.v)
            )
            return min_tuple

        def step2(i1: int, i2: int, i3: int):
            def v_abs_sqr(v: Coord) -> int:
                return sum(c * c for c in v)

            def test(p: Coord, v: Coord, s: Stone) -> int | None:
                dividend = s.p[1] * v[0] - p[1] * \
                    v[0] - v[1] * s.p[0] + v[1] * p[0]
                divisor = v[1] * s.v[0] - s.v[1] * v[0]
                if dividend % divisor != 0:
                    return None
                u = dividend // divisor
                if u < 0:
                    return None

                dividend = s.p[0] + u * s.v[0] - p[0]
                divisor = v[0]
                if dividend % divisor != 0:
                    return None
                t = dividend // divisor

                if p[2] + t * v[2] == s.p[2] + u * s.v[2]:
                    return t

                return None

            s1, s2, s3 = sorted(
                (stones[i1], stones[i2], stones[i3]),
                key=lambda s: s.abs_sqr,
                reverse=True
            )
            for t1 in range(10_000):
                if t1 % 100 == 0:
                    print(t1)
                s1_t1 = s1.pos(t1)
                for t2 in range(10_000):
                    s2_t2 = s2.pos(t2)
                    v12: Coord = diff(s1_t1, s2_t2)
                    v_gcd = gcd(*v12)
                    if v_gcd > 1:
                        v12 = (v12[0] // v_gcd, v12[1] //
                               v_gcd, v12[2] // v_gcd)

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
    else:
        """
        Get three stones with largest vectors and try to find a solution
        """
        stones = tuple(sorted(stones, key=lambda s: s.abs_sqr))
        print('smallest', stones[0])
        print('largest', stones[-1])

        def test(p: Coord, v: Coord, s: Stone) -> tuple[int, int] | None:
            numerator = s.p[1] * v[0] - p[1] * \
                v[0] - v[1] * s.p[0] + v[1] * p[0]
            denominator = v[1] * s.v[0] - s.v[1] * v[0]
            if numerator % denominator != 0:
                return None
            u = numerator // denominator

            numerator = s.p[0] + u * s.v[0] - p[0]
            denominator = v[0]

            if numerator % denominator != 0:
                return None
            t = numerator // denominator

            if p[2] + t * v[2] == s.p[2] + u * s.v[2]:
                return (t, u)

            return None

        s1, s2, s3 = stones[-1], stones[-2], stones[-3]

        def test_range(range_end: int, last_range_end: int):
            for t1 in range(range_end):
                if t1 % 100 == 0:
                    print(t1)
                s1_t1 = s1.pos(t1)
                for t2 in range(0 if t1 >= last_range_end else last_range_end, range_end):
                    s2_t2 = s2.pos(t2)
                    v12: Coord = diff(s1_t1, s2_t2)
                    v_gcd = gcd(*v12)
                    if v_gcd > 1:
                        v12 = (
                            v12[0] // v_gcd,
                            v12[1] // v_gcd,
                            v12[2] // v_gcd
                        )

                    t3 = test(s1_t1, v12, s3)
                    if t3 is not None:
                        print("Found solution", t1, t2, t3)
                        print("stones", s1, s2, s3)
                        exit()

        test_range(200_000, 100_000)

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

    # 686374601471592: too low

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
