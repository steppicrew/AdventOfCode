# https://adventofcode.com/2023/day/01
import re
from pathlib import Path

REF = 1
part_match = re.search(r'_(\d+)\.py', __file__)
part: str = "_" + part_match[1] if part_match else ""

EXT = "_ref" + str(REF) + ".txt" if REF else ".txt"
path = Path(__file__).parent.absolute()
with open(file=path/("input" + EXT), mode="r", encoding='utf-8') as file:
    inputs: list[str] = file.read().rstrip().split("\n")
# ---


def print_on(*args):
    print(*args)


def print_off(*args):  # pylint: disable=unused-argument
    pass


debug = print_on


def run() -> int:
    result: int = 0

    for input in inputs:
        debug(input)

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
