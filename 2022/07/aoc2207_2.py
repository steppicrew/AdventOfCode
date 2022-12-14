# https://adventofcode.com/2022/day/7
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

    sizes: dict[str, int] = {'': 0}
    dir = []
    result = 0
    for input in inputs:
        match = re.match(r'^\$ cd (\S+)', input)
        if match:
            if match[1] == '/':
                dir = []
            elif match[1] == '..':
                dir.pop()
            else:
                dir.append(match[1])
                sizes['/'.join(dir)] = 0
            continue
        match = re.match(r'^(\d+) ', input)
        if match:
            for i in range(len(dir)+1):
                sizes['/'.join(dir[:i])] += int(match[1])

    needed_space = 30_000_000 - (70_000_000 - sizes[''])

    candidates = [key for key in sizes.keys() if sizes[key] >= needed_space]
    candidates.sort(key=lambda key: sizes[key])
    print(list((candidate, sizes[candidate])for candidate in candidates))
    result = sizes[candidates[0]]

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
