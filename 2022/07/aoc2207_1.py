# https://adventofcode.com/2022/day/7
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

    candidates = [key for key in sizes.keys() if sizes[key] <= 100_000]
    for candidate in candidates:
        result += sizes[candidate]

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
