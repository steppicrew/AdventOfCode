# https://adventofcode.com/2022/day/13
from pathlib import Path
from functools import reduce
import re
from typing import Tuple
import json
import functools

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

    pairs: list = [[[2]], [[6]]]

    for input in inputs:
        if input:
            pairs.append(json.loads(input))

    sorted_pairs = sorted(
        pairs, key=functools.cmp_to_key(compare), reverse=True)

    result = (sorted_pairs.index([[2]]) + 1) * (sorted_pairs.index([[6]]) + 1)

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
