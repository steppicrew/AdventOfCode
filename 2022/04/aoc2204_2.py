# https://adventofcode.com/2022/day/4
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
    for input in inputs:
        (elf1range, elf2range) = input.split(",")
        (elf1start, elf1stop) = elf1range.split("-")
        (elf2start, elf2stop) = elf2range.split("-")
        elf1 = set(range(int(elf1start), int(elf1stop)+1))
        elf2 = set(range(int(elf2start), int(elf2stop)+1))
        if len(elf1.intersection(elf2)):
            result += 1

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
