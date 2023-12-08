# https://adventofcode.com/2023/day/01
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

    position = 'AAA'
    steps = 0
    while True:
        if position == 'ZZZ':
            break

        direction = directions.pop(0)
        directions.append(direction)
        position = navigation[position][direction]
        steps += 1

    result = steps
    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
