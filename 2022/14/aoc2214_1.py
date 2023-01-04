# https://adventofcode.com/2022/day/14
from pathlib import Path
from functools import reduce
import re
from typing import Tuple
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

    map: set[Tuple[int, int]] = set()

    def build_coords(pair: str):
        coords = pair.split(",")
        return (int(coords[0]), int(coords[1]))

    max_y = 0

    for input in inputs:
        pairs = input.split(' -> ')
        xy = build_coords(pairs[0])
        max_y = xy[1]
        map.add(xy)
        for pair in pairs[1:]:
            end_xy = build_coords(pair)
            if max_y < end_xy[1]:
                max_y = end_xy[1]
            dx = 0 if xy[0] == end_xy[0] else (
                int((end_xy[0] - xy[0]) / abs(end_xy[0] - xy[0])))
            dy = 0 if xy[1] == end_xy[1] else (
                int((end_xy[1] - xy[1]) / abs(end_xy[1] - xy[1])))
            while xy != end_xy:
                xy = (xy[0] + dx, xy[1] + dy)
                map.add(xy)

    sand_count = 0
    abyss = False
    while not abyss:
        sand_pos = (500, 0)
        if sand_pos in map:
            break
        while True:
            (x, y) = sand_pos
            if (x, y + 1) not in map:
                sand_pos = (x, y + 1)
            elif (x - 1, y + 1) not in map:
                sand_pos = (x - 1, y + 1)
            elif (x + 1, y + 1) not in map:
                sand_pos = (x + 1, y + 1)
            else:
                map.add(sand_pos)
                sand_count += 1
                break
            if sand_pos[1] > max_y:
                print("abyss", sand_pos, max_y)
                abyss = True
                break

    result = sand_count

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
