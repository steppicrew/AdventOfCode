# https://adventofcode.com/2022/day/13
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

    def compare(left, right):
        tl = type(left)
        tr = type(right)
        if tl != tr:
            return compare(left if tl == list else [left], right if tr == list else [right])
        if tl == list:
            for i, lv in enumerate(left):
                if i >= len(right):
                    return -1
                r = compare(lv, right[i])
                if r != 0:
                    return r
            if len(left) == len(right):
                return 0
            else:
                return 1
        else:
            if left < right:
                return 1
            if left > right:
                return -1
            return 0

    pairs: list = [[]]

    for input in inputs:
        if not input:
            pairs.append([])
        else:
            pairs[-1].append(json.loads(input))

    for i, pair in enumerate(pairs):
        if compare(pair[0], pair[1]) == 1:
            result += i + 1

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
