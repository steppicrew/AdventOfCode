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


def print_off(*args):  # pylint: disable=unused-argument
    pass


debug = print


def run() -> int:
    result: int = 0

    Position = tuple[int, int]

    field: tuple[str, ...] = tuple(line.replace("S", ".") for line in inputs)
    visited: dict[Position, int] = {}
    start: Position | None = None

    for l, input in enumerate(inputs):
        start_index = input.find("S")
        if start_index >= 0:
            start = (l, start_index)
            break
    assert start is not None

    reached: list[Position] = [start]

    def add_if_reachable(x: int, y: int, list_to_add: list[Position], step: int) -> None:
        if (x, y) in visited:
            return
        if 0 <= x < len(field[0]) and 0 <= y < len(field):
            if field[y][x] != '#':
                list_to_add.append((x, y))
                visited[(x, y)] = step

    for step in range(64):
        new_reached: list[Position] = []
        for pos in reached:
            add_if_reachable(pos[0]+1, pos[1], new_reached, step)
            add_if_reachable(pos[0]-1, pos[1], new_reached, step)
            add_if_reachable(pos[0], pos[1]+1, new_reached, step)
            add_if_reachable(pos[0], pos[1]-1, new_reached, step)
        reached = new_reached

    debug(visited)

    result = len([v for v in visited.values() if v % 2 == 1])

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
