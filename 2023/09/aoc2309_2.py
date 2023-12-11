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

    for input in inputs:  # pylint: disable=[redefined-builtin]
        diffs: list[list[int]] = [
            [int(v) for v in reversed(re.findall(r'\-?\d+', input))]]
        while [d for d in diffs[-1] if d != 0]:
            diffs.append(
                [
                    v - diffs[-1][i - 1]
                    for i, v in enumerate(diffs[-1])
                    if i > 0
                ]
            )

        diffs[-1].append(0)

        for i in range(len(diffs)-1, 0, -1):
            diffs[i-1].append(diffs[i][-1] + diffs[i-1][-1])

        result += diffs[0][-1]

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
