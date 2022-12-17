# https://adventofcode.com/2022/day/10
from pathlib import Path
from functools import reduce
import re
from typing import Callable, Tuple

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():

    _tick = 0
    x = 1
    result = 0
    crt: list[bool] = []

    def tick():
        nonlocal _tick
        crt.append(_tick % 40 >= x-1 and _tick % 40 <= x+1)
        _tick += 1

    for input in inputs:
        tick()
        if input == 'noop':
            pass
        else:
            match = re.match(r'addx (\-?\d+)', input)
            if match:
                tick()
                x += int(match[1])

    for i in range(0, len(crt), 40):
        print(''.join(['#' if p else '.' for p in crt[i:i+40]]))

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
