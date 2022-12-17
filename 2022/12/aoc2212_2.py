# https://adventofcode.com/2022/day/12
from pathlib import Path
from functools import reduce
import re
from typing import Tuple

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():
    result = 0

    infinity: int = 100_000_000_000

    heights: dict[Tuple[int, int], int] = dict()
    data: dict[Tuple[int, int], Tuple[int, Tuple[int, int]]] = dict()

    visited: set[tuple[int, int]] = set()

    len_x = len(inputs[0])
    len_y = len(inputs)

    start: Tuple[int, int] = (0, 0)
    end: Tuple[int, int] = (0, 0)
    for y, input in enumerate(inputs):
        for x, c in enumerate(input):
            xy = (x, y)
            if c == 'S':
                c = 'a'
                end = xy
            if c == 'E':
                c = 'z'
                start = xy
            heights[xy] = ord(c) - ord('a')
            data[xy] = (infinity, (0, 0))

    data[start] = (0, start)

    def get_candidates(xy: Tuple[int, int]) -> Tuple[Tuple[int, int]]:
        (x, y) = xy
        candidates = tuple(
            _xy for _xy in ((x-1, y), (x+1, y), (x, y-1), (x, y+1))
            if _xy[0] >= 0 and _xy[0] < len_x and _xy[1] >= 0 and _xy[1] < len_y
        )

        min_height = heights[xy] - 1
        return tuple(_xy for _xy in candidates if _xy not in visited and heights[_xy] >= min_height)

    xy = start
    while True:
        visited.add(xy)
        next_dist = data[xy][0] + 1
        for _xy in get_candidates(xy):
            if data[_xy][0] > next_dist:
                data[_xy] = (next_dist, xy)

        not_visited = list(xy for xy in heights.keys()
                           if xy not in visited and data[xy][0] < infinity)
        if not not_visited:
            break
        not_visited.sort(key=lambda xy: data[xy][0])
        xy = not_visited[0]

    if data[end][0] == infinity:
        print("Could not find path")
    else:
        a_level = [xy for xy in heights.keys() if heights[xy] == 0]
        a_level.sort(key=lambda xy: data[xy][0])
        result = data[a_level[0]][0]

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
