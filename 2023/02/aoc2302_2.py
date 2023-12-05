# https://adventofcode.com/2023/day/01
import re
from math import prod
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

    for input in inputs:  # pylint: disable=[redefined-builtin]
        if not input.strip():
            continue

        max_draws: dict[str, int] = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }

        _, line = input.split(':', 1)
        draws = line.split(';')
        for draw in draws:
            for color_draw in draw.split(','):
                match = re.search(r'(\d+) (\w+)', color_draw)
                assert match is not None
                max_draws[match.group(2)] = max(
                    max_draws[match.group(2)],
                    int(match.group(1))
                )
        result += prod(max_draws.values())

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
