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

    field: list[list[str]] = []

    for input in inputs[:]:  # pylint: disable=[redefined-builtin]
        field.append([i for i in input])

    def move(c: int, rs: int, rd: int):
        place = field[rs][c]
        field[rs][c] = '.'
        field[rd][c] = place

    for c in range(len(field[0])):
        column = ''.join(l[c] for l in field)

        for r, place in enumerate(column):
            if place != 'O' or r == 0 or field[r-1][c] != '.':
                continue
            r2 = r-1
            while r2 > 0 and field[r2-1][c] == '.':
                r2 -= 1
            if field[r2][c] == '.':
                move(c, r, r2)

    text_field = [''.join(l) for l in field]

    for i, line in enumerate(text_field):
        result += line.count('O') * (len(text_field) - i)

    print('\n'.join(text_field))

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
