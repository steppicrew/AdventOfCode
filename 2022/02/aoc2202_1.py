# https://adventofcode.com/2022/day/2
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
        (opponent, me) = input.split(" ", maxsplit=2)
        opponent = ord(opponent) - ord('A')
        me = ord(me) - ord('X')
        result += me+1
        if (me + 1) % 3 == opponent:
            result += 0
        elif(opponent+1) % 3 == me:
            result += 6
        else:
            result += 3

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
