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

    add_rows = 0
    galaxies: list[tuple[int, int]] = []
    for i, input in enumerate(inputs):  # pylint: disable=[redefined-builtin]
        if input.count('.') == len(input):
            add_rows += 1
            continue
        start = 0
        while match := re.search(r'#', input[start:]):
            galaxies.append((start + match.start(), i + add_rows))
            start += match.start()+1

    add_cols = 0
    for i, _ in enumerate(inputs[0]):
        col = ''.join(r[i] for r in inputs)
        if col.count('.') == len(col):
            for j, galaxy in enumerate(galaxies):
                if galaxy[0] > i + add_cols:
                    galaxies[j] = (galaxy[0] + 1, galaxy[1])
            add_cols += 1

    for i, galaxy1 in enumerate(galaxies):
        for galaxy2 in galaxies[i+1:]:
            dist = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
            result += dist

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
