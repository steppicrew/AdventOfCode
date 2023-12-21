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


def print_off(*args):  # pylint: disable=unused-argument
    pass


debug = print


def run() -> int:
    result: int = 0

    Position = tuple[int, int]

    field: tuple[str, ...] = tuple(line.replace("S", ".") for line in inputs)
    start: Position | None = None

    for l, input in enumerate(inputs):
        start_index = input.find("S")
        if start_index >= 0:
            start = (l, start_index)
            break
    assert start is not None

    def test_from_start(start: Position, visited: dict[Position, tuple[int, int]], start_step: int):
        reached: list[Position] = [start]
        visited[start] = (start_step, 0)

        def add_if_reachable(x: int, y: int, list_to_add: list[Position], step: int) -> None:
            if (x, y) in visited and start_step + step >= visited[(x, y)][0] + visited[(x, y)][1]:
                return
            if 0 <= x < len(field[0]) and 0 <= y < len(field):
                if field[y][x] != '#':
                    list_to_add.append((x, y))
                    visited[(x, y)] = (start_step, step)

        step = 0
        while True:
            step += 1
            new_reached: list[Position] = []
            for pos in reached:
                add_if_reachable(pos[0]+1, pos[1], new_reached, step)
                add_if_reachable(pos[0]-1, pos[1], new_reached, step)
                add_if_reachable(pos[0], pos[1]+1, new_reached, step)
                add_if_reachable(pos[0], pos[1]-1, new_reached, step)
            if not reached:
                break
            reached = new_reached

    visited: dict[str, dict[Position, tuple[int, int]]] = {
        "start": {},
        "north": {},
        "south": {},
        "west": {},
        "east": {},
    }

    test_from_start(start, visited["start"], 0)

    for x in range(len(field[0])):
        if field[0][x] != '#' and field[-1][x] != '#':
            north = (x, 0)
            south = (x, len(field)-1)
            test_from_start(
                north, visited["south"], visited["start"][south][1] + 1
            )
            test_from_start(
                south, visited["north"], visited["start"][north][1] + 1
            )

    for y, line in enumerate(field):
        if line[0] != '#' and line[-1] != '#':
            west = (0, y)
            east = (len(field[0])-1, y)
            test_from_start(
                west, visited["east"], visited["start"][east][1] + 1
            )
            test_from_start(
                east, visited["west"], visited["start"][west][1] + 1
            )

    min_east = min(visited["east"][(len(field[0]) - 1, y)][1]
                   for y in range(len(field)))
    min_west = min(visited["west"][(0, y)][1] for y in range(len(field)))
    min_south = min(visited["south"][x, (len(field) - 1)][1]
                    for x in range(len(field[0])))
    min_north = min(visited["north"][(x, 0)][1] for x in range(len(field[0])))

    debug("min_east", min_east, max(v[1] for v in visited["east"].values()))
    debug("min_west", min_west, max(v[1] for v in visited["west"].values()))
    debug("min_north", min_north, max(v[1] for v in visited["north"].values()))
    debug("min_south", min_south, max(v[1] for v in visited["south"].values()))
    debug(len(field), len(field[0]))
    debug([v for p, v in visited["east"].items() if p[0] == len(field[0]) - 1])

    for name, v in visited.items():
        debug("len", name, len(v))

    # result = len([v for v in visited.values() if v % 2 == 1])

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
