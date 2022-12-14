# https://adventofcode.com/2022/day/6
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
    result = 0
    input = inputs[0]
    i = 0
    while True:
        marker = input[i:i+14]
        if len(set(marker)) == 14:
            result = i+14
            break
        i += 1

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
