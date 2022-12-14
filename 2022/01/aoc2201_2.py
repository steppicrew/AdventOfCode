# https://adventofcode.com/2022/day/1
from pathlib import Path
from functools import reduce

ref = 0
part = "_1"

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():
    result = 0
    calories: list[int] = [0]
    for input in inputs:
        if input:
            calories[-1] += int(input)
        else:
            calories.append(0)

    calories.sort(reverse=True)
    result = calories[0] + calories[1] + calories[2]

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
