# https://adventofcode.com/2022/day/18
from pathlib import Path
from functools import reduce
import re
from typing import Callable, Tuple
import json

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():
    result = 0

    room: set[tuple[int, int, int]] = set()

    for input in inputs:
        coords = [int(c) for c in input.split(',')]
        room.add((coords[0], coords[1], coords[2]))

    result = 6 * len(room)
    for c in room:
        x, y, z = c
        for c2 in ((x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1)):
            if c2 in room:
                result -= 1

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
