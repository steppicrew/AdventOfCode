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
    visible = {}
    for input in inputs:
        trees.append([int(c) for c in input])

    for row in range(len(trees)):
        cols = list(range(len(trees[0])))
        max = -1
        for col in cols:
            if trees[row][col] > max:
                max = trees[row][col]
                visible[(row, col)] = True
        max = -1
        cols.reverse()
        for col in cols:
            if trees[row][col] > max:
                max = trees[row][col]
                visible[(row, col)] = True

    for col in range(len(trees[0])):
        rows = list(range(len(trees)))
        max = -1
        for row in rows:
            if trees[row][col] > max:
                max = trees[row][col]
                visible[(row, col)] = True
        max = -1
        rows.reverse()
        for row in rows:
            if trees[row][col] > max:
                max = trees[row][col]
                visible[(row, col)] = True

    result = len(visible)

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
