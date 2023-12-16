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

    def follow(pos: tuple[int, int], dir: tuple[int, int]) -> int:
        energized: dict[tuple[int, int], set[tuple[int, int]]] = {}
        starts: list[tuple[tuple[int, int], tuple[int, int]]] = [(pos, dir)]
        while starts:
            pos, dir = starts.pop()

            while 0 <= pos[0] < len(field[0]) and 0 <= pos[1] < len(field):
                if not pos in energized:
                    energized[pos] = set((dir,))
                elif dir in energized[pos]:
                    break
                else:
                    energized[pos].add(dir)

                tile = field[pos[1]][pos[0]]
                if tile == '|' and dir[0] != 0:
                    starts.append((pos, (0, -dir[0])))
                    tile = '\\'
                elif tile == '-' and dir[1] != 0:
                    starts.append((pos, (-dir[1], 0)))
                    tile = '\\'

                if tile == '\\':
                    dir = (dir[1], dir[0])
                elif tile == '/':
                    dir = (-dir[1], -dir[0])

                pos = (pos[0] + dir[0], pos[1] + dir[1])

        return len(energized)

    result = follow((0, 0), (1, 0))

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
