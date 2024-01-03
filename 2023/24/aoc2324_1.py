# https://adventofcode.com/2023/day/01
import re
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


def run() -> int:
    result: int = 0

    Stone3d = tuple[tuple[int, int, int], tuple[int, int, int]]
    Stone2d = tuple[tuple[int, int], tuple[int, int],
                    tuple[float, float] | tuple[None, None]]

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

    # m1*x + n1 = m2*x + n2
    # (m1 - m2)*x = n2 - n1
    # x = (n2 - n1) / (m1 - m2)

    def get_mn(xy: tuple[int, int, int], dxy: tuple[int, int, int]) -> tuple[float, float] | tuple[None, None]:
        if dxy[0] == 0:
            return (None, None)
        m = dxy[1] / dxy[0]
        n = xy[1] - m * xy[0]
        return (m, n)

    stones2d: tuple[Stone2d, ...] = tuple(
        (
            (stone[0][0], stone[0][1]),
            (stone[1][0], stone[1][1]),
            get_mn(stone[0], stone[1])
        )
        for stone in stones3d
    )

    test_range = (7, 27) if REF == 1 else (200000000000000, 400000000000000)

    for i, stone1 in enumerate(stones2d):
        for stone2 in stones2d[i+1:]:
            if stone1 == stone2:
                continue

            assert stone1[2] != (None, None) and stone2[2] != (None, None)

            if stone1[2][0] == stone2[2][0]:
                if stone1[2][1] == stone2[2][1]:
                    result += 1
                continue

            assert stone1[2][0] is not None
            assert stone1[2][1] is not None
            assert stone2[2][0] is not None
            assert stone2[2][1] is not None

            x = (stone2[2][1] - stone1[2][1]) / (stone1[2][0] - stone2[2][0])
            y = stone1[2][0] * x + stone1[2][1]

            t1 = (x - stone1[0][0]) / stone1[1][0]
            if t1 < 0:
                continue

            t2 = (x - stone2[0][0]) / stone2[1][0]
            if t2 < 0:
                continue

            if test_range[0] <= x <= test_range[1] and test_range[0] <= y <= test_range[1]:
                debug(stone1, stone2)
                debug(t1, t2, x, y)
                result += 1

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
