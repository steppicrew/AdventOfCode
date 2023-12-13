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

    field: list[str] = []

    def line_to_int(line: str) -> int:
        return int(''.join('0' if c == '.' else '1' for c in line), base=2)

    def parse_field(_field: list[str]) -> int:
        field = [line_to_int(l) for l in _field]
        for i in range(1, len(field)):
            max_rows = min(i, len(field) - i)
            diff = 0
            # print("Testing line", i, max_rows)
            for r in range(0, max_rows):
                line1 = field[i-r-1]
                line2 = field[i+r]

                _diff = bin(line1 ^ line2).count('1')
                diff += _diff

                # print(_field[i-r-1])
                # print(_field[i+r], _diff)

                if diff > 1:
                    break
            if diff == 1:
                return i
        return 0

    def flipped(field: list[str]) -> list[str]:
        return [
            ''.join(
                field[r][c] for r, _ in enumerate(field)
            )
            for c, _ in enumerate(field[0])
        ]

    for input in inputs[:] + ['']:  # pylint: disable=[redefined-builtin]
        if not input:
            hor = parse_field(field)
            ver = parse_field(flipped(field))

            # print(field, hor, ver)

            result += hor * 100
            result += ver
            field = []
            continue
        field.append(input)

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
