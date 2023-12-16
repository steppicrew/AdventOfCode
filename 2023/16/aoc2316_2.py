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


def run() -> int:
    result: int = 0

    field: tuple[str, ...] = tuple(inputs)
    energized: dict[tuple[int, int], list[tuple[int, int]]] = {}

    def _follow(pos: tuple[int, int], dir: tuple[int, int]):
        while pos[0] >= 0 and pos[0] < len(field[0]) and pos[1] >= 0 and pos[1] < len(field):
            if not pos in energized:
                energized[pos] = []

            if dir in energized[pos]:
                return

            energized[pos].append(dir)

            tile = field[pos[1]][pos[0]]
            if tile == '|' and dir[0] != 0:
                _follow(pos, (0, -dir[0]))
                tile = '\\'
            elif tile == '-' and dir[1] != 0:
                _follow(pos, (-dir[1], 0))
                tile = '\\'

            if tile == '\\':
                dir = (dir[1], dir[0])
            elif tile == '/':
                dir = (-dir[1], -dir[0])

            pos = (pos[0] + dir[0], pos[1] + dir[1])

    def follow(pos: tuple[int, int], dir: tuple[int, int]):
        energized.clear()
        _follow(pos, dir)
        return len(energized)

    for x in range(len(field[0])):
        result = max(
            result,
            follow((x, 0), (0, 1)),
            follow((x, len(field) - 1), (0, -1))
        )

    for y in range(len(field)):
        result = max(
            result,
            follow((0, y), (1, 0)),
            follow((len(field[0]) - 1, y), (-1, 0))
        )

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
