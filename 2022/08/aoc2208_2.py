# https://adventofcode.com/2022/day/8
from pathlib import Path
from functools import reduce
import re
from typing import Iterator, Tuple

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():

    trees: list[list[int]] = []
    for input in inputs:
        trees.append([int(c) for c in input])

    max_score = 0
    rows = len(trees)
    cols = len(trees[0])
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            height = trees[row][col]
            this_score = 1

            def get_count(it: Iterator[Tuple[int, int]]) -> int:
                count = 0
                for (row, col) in it:
                    count += 1
                    if trees[row][col] >= height:
                        break
                return count

            this_score *= get_count((row, c) for c in range(col+1, cols))
            this_score *= get_count((row, c) for c in reversed(range(col)))
            this_score *= get_count((r, col) for r in range(row+1, rows))
            this_score *= get_count((r, col) for r in reversed(range(row)))

            if this_score > max_score:
                max_score = this_score

    result = max_score

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
