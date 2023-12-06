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
    result: int = 1  # pylint: disable=[redefined-outer-name]

    time_distances = zip(
        (int(t) for t in re.findall(r'\d+', inputs[0].replace(" ", ""))),
        (int(d) for d in re.findall(r'\d+', inputs[1].replace(" ", "")))
    )

    for time, distance in time_distances:

        count = 0
        for t in range(1, time):
            if t * (time - t) > distance:
                count += 1
        result *= count

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
