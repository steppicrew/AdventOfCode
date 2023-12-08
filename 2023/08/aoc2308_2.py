# https://adventofcode.com/2023/day/01
import math
import re
from pathlib import Path

REF = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part: str = "_" + part_match[1] if part_match else ""

EXT = "_ref" + str(REF) + ".txt" if REF else ".txt"
path = Path(__file__).parent.absolute()
with open(file=path/("input" + EXT), mode="r", encoding='utf-8') as file:
    inputs: list[str] = file.read().rstrip().split("\n")
# ---


def run() -> int:  # pylint: disable=[missing-function-docstring]
    result: int = 0  # pylint: disable=[redefined-outer-name]

    directions = [(0 if d == 'L' else 1) for d in inputs[0]]
    navigation: dict[str, tuple[str, str]] = {}

    for input in inputs[2:]:  # pylint: disable=[redefined-builtin]
        if match := re.match(r'\s*(\w\w\w)\s*=\s*\(\s*(\w\w\w)\s*,\s*(\s*\w\w\w)\s*\)', input):
            navigation[match.group(1)] = (match.group(2), match.group(3))

    positions = [p for p in navigation if p[-1] == 'A']

    dir_len = len(directions)
    p_ends: list[tuple[int, int]] = []
    for p in positions:
        step = 0
        zs: list[int] = []
        while True:
            if p[-1] == 'Z':
                zs.append(step)
                if len(zs) == 2:
                    break
            direction = directions[step % dir_len]
            p = navigation[p][direction]
            step += 1

        p_ends.append((2 * zs[0]-zs[1], zs[1] - zs[0]))

    offsets: dict[int, int] = {}
    for pe in p_ends:
        if pe[0] not in offsets:
            offsets[pe[0]] = pe[1]
        else:
            offsets[pe[0]] = math.lcm(offsets[pe[0]], pe[1])

    max_lcm = max(offsets.values())
    max_offset = [key for key in offsets if offsets[key] == max_lcm][0]

    n = 1
    while True:
        step = max_offset + n * max_lcm
        if len([1 for offset, lcm in offsets.items() if (step - offset) % lcm != 0]) == 0:
            break
        n += 1

    result = step
    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
