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

    def tick():
        nonlocal _tick
        _tick += 1
        if (_tick - 20) % 40 == 0:
            nonlocal result
            result += _tick * x

    for input in inputs:
        tick()
        if input == 'noop':
            pass
        else:
            match = re.match(r'addx (\-?\d+)', input)
            if match:
                tick()
                x += int(match[1])

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
