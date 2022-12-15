# https://adventofcode.com/2022/day/3
from pathlib import Path
from functools import reduce
import re

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():
    result = 0
    for input in inputs:
        contents = list(input)
        bag1 = set(contents[:int(len(contents)/2)])
        bag2 = set(contents[int(len(contents)/2):])
        common = ord(list(bag1.intersection(bag2))[0])-ord('A')
        if common > 25:
            common += ord('A') - ord('a') + 1
        else:
            common += 27

        result += common

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
