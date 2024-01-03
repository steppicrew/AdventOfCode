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
        if v1[0] == 0:
            return False
        if v2[1] == v2[0]*v1[1]/v1[0]:
            return False
        t = (p1[1] + p2[0]*v1[1]/v1[0] - p1[0]*v1[1] /
             v1[0] - p2[1]) / (v2[1] - v2[0]*v1[1]/v1[0])
        s = (p2[0] + t*v2[0] - p1[0]) / v1[0]
        # debug(s, t)
        return p1[2] + s * v1[2] == p2[2] + t * v2[2]

    for i, s1 in enumerate(stones3d):
        for s2 in stones3d[i+1:]:
            if test_intersection(s1, s2):
                debug(s1, s2)
                exit()
    # debug(test_intersection(((0, 0, 0), (1, 1, 1)), ((0, 1, 1), (1, 0, 0))))

    def dot_prod(f1: tuple[int, int, int], f2: tuple[int, int, int]) -> int:
        return sum(x*y for x, y in zip(f1, f2))

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
