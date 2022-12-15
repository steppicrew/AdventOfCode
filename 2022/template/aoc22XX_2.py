# https://adventofcode.com/2022/day/03
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
        pass

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
