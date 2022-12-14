# https://adventofcode.com/2022/day/8
from pathlib import Path
from functools import reduce
import re

ref = 0
part = "_1"

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

            count = 0
            for c in range(col+1, cols):
                count += 1
                if trees[row][c] >= height:
                    break
            this_score *= count

            count = 0
            left = list(range(col))
            left.reverse()
            for c in left:
                count += 1
                if trees[row][c] >= height:
                    break
            this_score *= count

            count = 0
            for r in range(row+1, rows):
                count += 1
                if trees[r][col] >= height:
                    break
            this_score *= count

            count = 0
            up = list(range(row))
            up.reverse()
            for r in up:
                count += 1
                if trees[r][col] >= height:
                    break
            this_score *= count

            if this_score > max_score:
                max_score = this_score

    result = max_score

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
