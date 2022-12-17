# https://adventofcode.com/2022/day/9
from pathlib import Path
from functools import reduce
import re
from typing import Callable, Tuple

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():

    def sign(x):
        if x > 0:
            return 1
        if x < 0:
            return -1
        return 0

    head = (0, 0)
    tail = (0, 0)
    tail_positions: set[Tuple[int, int]] = set()

    for input in inputs:
        (dir, count) = input.split(None)
        count = int(count)
        if dir == 'U':
            dir = (0, 1)
        elif dir == 'R':
            dir = (1, 0)
        elif dir == 'D':
            dir = (0, -1)
        elif dir == 'L':
            dir = (-1, 0)
        else:
            assert None

        for _ in range(count):
            head = (head[0] + dir[0], head[1] + dir[1])
            diff0 = head[0]-tail[0]
            diff1 = head[1]-tail[1]
            if abs(diff0) > 1 or abs(diff1) > 1:
                tail = (tail[0]+sign(diff0), tail[1]+sign(diff1))
            tail_positions.add(tail)

    result = len(tail_positions)

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
