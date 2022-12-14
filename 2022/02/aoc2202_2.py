# https://adventofcode.com/2022/day/2
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
        (opponent, score) = input.split(" ", maxsplit=2)
        opponent = ord(opponent) - ord('A')
        score = ord(score) - ord('X')
        me = (opponent + score - 1) % 3

        result += me + 1 + score * 3

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
