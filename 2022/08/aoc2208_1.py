# https://adventofcode.com/2022/day/8
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

    trees: list[list[int]] = []
    visible: set[Tuple[int, int]] = set()

    def get_visible(outer: list[int], inner: list[int], to_col_row: Callable[[int, int], Tuple[int, int]]) -> None:
        for o in outer:
            max = -1
            for i in inner:
                (row, col) = to_col_row(o, i)
                if trees[row][col] > max:
                    max = trees[row][col]
                    visible.add((row, col))

    for input in inputs:
        trees.append([int(c) for c in input])

    rows = list(range(len(trees)))
    cols = list(range(len(trees[0])))

    get_visible(rows, cols, lambda r, c: (r, c))
    cols.reverse()
    get_visible(rows, cols, lambda r, c: (r, c))
    get_visible(cols, rows, lambda c, r: (r, c))
    rows.reverse()
    get_visible(cols, rows, lambda c, r: (r, c))

    result = len(visible)

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
