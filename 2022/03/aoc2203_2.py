# https://adventofcode.com/2022/day/3
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
    for i in range(int(len(inputs)/3)):
        common = ord(list(set(inputs[3*i]).intersection(
            inputs[3*i+1]).intersection(inputs[3*i+2]))[0])-ord('A')
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
