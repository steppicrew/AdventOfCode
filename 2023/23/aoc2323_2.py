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
debug_off = print_off


def run() -> int:
    result: int = 0

    Coord = tuple[int, int]

    def get_neighbors(x: int, y: int) -> tuple[Coord, ...]:
        result: list[Coord] = []
        if x > 0 and inputs[y][x-1] != '#':
            result.append((x-1, y))
        if x < len(inputs[0]) - 1 and inputs[y][x+1] != '#':
            result.append((x+1, y))
        if y > 0 and inputs[y-1][x] != '#':
            result.append((x, y-1))
        if y < len(inputs) - 1 and inputs[y+1][x] != '#':
            result.append((x, y+1))
        # debug(x, y, result)
        return tuple(result)

    field: dict[Coord, tuple[Coord, ...]] = {
        (x, y): get_neighbors(x, y)
        for y in range(len(inputs))
        for x in range(len(inputs[0]))
        if inputs[y][x] != '#'
    }

    start = (inputs[0].find('.'), 0)
    end = (inputs[-1].find('.'), len(inputs)-1)

    all_junctions = {
        p: n
        for p, n in field.items()
        if len(n) > 2
    }
    all_junctions[start] = field[start]
    all_junctions[end] = field[end]
    junction_neighbours: dict[Coord, dict[Coord, int]] = {}

    for junction in all_junctions:
        neighbours: dict[Coord, int] = {}
        junction_neighbours[junction] = neighbours

        for start_pos in field[junction]:
            last_pos = junction
            pos = start_pos
            count = 1
            while pos not in all_junctions:
                count += 1
                _nexts = field[pos]
                next_index = 1 if _nexts[0] == last_pos else 0
                last_pos = pos
                pos = _nexts[next_index]
            if pos != junction:
                if pos not in neighbours or neighbours[pos] < count:
                    neighbours[pos] = count

    queue: list[tuple[Coord, tuple[Coord, ...], int]] = [
        (start, (start,), 0)
    ]

    end_tail: tuple[Coord, ...] = ()
    max_end_tail: int = 0

    debug(junction_neighbours[start])

    count = 0
    while queue:
        count += 1
        queue.sort(key=lambda qe: qe[2], reverse=True)
        pos, tail, cost = queue.pop(0)
        for next_pos, next_cost in junction_neighbours[pos].items():
            if next_pos in tail:
                continue
            new_cost = cost + next_cost
            new_tail = tuple((*tail, next_pos))
            queue.append((next_pos, new_tail, new_cost))
            if next_pos == end:
                if new_cost > max_end_tail:
                    max_end_tail = new_cost
                    end_tail = new_tail
        # debug(tail, cost, len(queue))
        if count % 100000 == 0:
            debug(count, len(queue), max_end_tail)

    debug(end_tail, max_end_tail)

    result = max_end_tail

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
