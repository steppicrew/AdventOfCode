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

    symbols: dict[tuple[int, int], list[int]] = {}
    symbol_re = r'\*'

    # find all symbols
    for line, input in enumerate(inputs):  # pylint: disable=[redefined-builtin]
        start = 0
        while match := re.search(symbol_re, input[start:]):
            symbols[(line, start + match.start(0))] = []
            start += match.end(0)

    # find all numbers
    for line, input in enumerate(inputs):  # pylint: disable=[redefined-builtin]
        start = 0
        while match := re.search(r'\d+', input[start:]):
            number = int(match.group(0))
            for x in range(start + match.start(0) - 1, start + match.end(0) + 1):
                for y in [line - 1, line, line + 1]:
                    if (y, x) in symbols:
                        symbols[(y, x)].append(number)
            start += match.end(0)

    for numbers in symbols.values():
        if len(numbers) < 2:
            continue
        result += prod(numbers)

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
