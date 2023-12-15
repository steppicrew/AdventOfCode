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

    cycles = 1_000_000_000

    for input in inputs[:]:  # pylint: disable=[redefined-builtin]
        field.append([i for i in input])

    def field_to_tuple(field: list[list[str]]) -> tuple[str, ...]:
        return tuple(''.join(l) for l in field)

    def move_north(field: list[list[str]]):
        def swap(c: int, rs: int, rd: int):
            field[rs][c], field[rd][c] = (field[rd][c], field[rs][c])

        for c in range(len(field[0])):
            column = ''.join(l[c] for l in field)

            for r, place in enumerate(column):
                if place != 'O' or r == 0 or field[r-1][c] != '.':
                    continue
                r2 = r-1
                while r2 > 0 and field[r2-1][c] == '.':
                    r2 -= 1
                if field[r2][c] == '.':
                    swap(c, r, r2)

    def rotate_right(field: list[list[str]]):
        return [
            [
                l[c] for l in reversed(field)
            ]
            for c in range(len(field[0]))
        ]

    def cycle(field: list[list[str]]):
        for _ in range(4):
            move_north(field)
            field = rotate_right(field)
        return field

    def run_cycles(field: list[list[str]], cycles: int) -> tuple[int, int, list[list[str]]]:

        cache: dict[tuple[str, ...], int] = {}

        text_field = ("")
        for c in range(cycles):
            field = cycle(field)

            text_field = field_to_tuple(field)
            if text_field in cache:
                return (cache[text_field], c, field)

            cache[text_field] = c

        assert False

    start, end, field = run_cycles(field, cycles)
    remainder = (cycles - start - 1) % (end - start)

    for i in range(remainder):
        field = cycle(field)

    text_field = field_to_tuple(field)

    for i, line in enumerate(text_field):
        result += line.count('O') * (len(text_field) - i)

    # print('\n'.join(text_field))
    # print(len(text_field), len(text_field[0]))

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
