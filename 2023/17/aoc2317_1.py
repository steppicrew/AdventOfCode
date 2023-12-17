# https://adventofcode.com/2023/day/01
import re
from pathlib import Path
from typing import Literal

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

    Position = tuple[int, int]
    Direction = tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]]

    INFINITY = 10_000_000

    ALL_DIRECTIONS = False

    field: tuple[tuple[int, ...], ...] = tuple(
        tuple(int(c) for c in l)
        for l in inputs
    )

    dest: Position = (len(field[0]) - 1, len(field) - 1)

    def add_dir(pos: Position, dir: Direction) -> Position:
        return (pos[0] + dir[0], pos[1] + dir[1])

    def abs_dir(dir: Direction) -> Direction:
        return (1 if dir[0] != 0 else 0, 1 if dir[1] != 0 else 0)

    def visited_key(pos: Position, dir: Direction) -> tuple[Position, Direction]:
        return (pos, dir) if ALL_DIRECTIONS else (pos, abs_dir(dir))

    def valid_pos(pos: Position) -> bool:
        return 0 <= pos[0] < len(field[0]) and 0 <= pos[1] < len(field)

    def get_field_cost(pos: Position) -> int:
        return field[pos[1]][pos[0]] if valid_pos(pos) else INFINITY

    _cost_cache: dict[tuple[Position, Direction], tuple[int, tuple[Position, ...]]] = {
        ((1, 0), (1, 0)): (get_field_cost((1, 0)), ()),
        ((0, 1), (0, 1)): (get_field_cost((0, 1)), ())
    }

    def get_cost_tail(pos: Position, dir: Direction) -> tuple[int, tuple[Position, ...]]:
        key = visited_key(pos, dir)
        return _cost_cache[key] if key in _cost_cache else (INFINITY, ())

    def get_cost(pos: Position, dir: Direction) -> int:
        return get_cost_tail(pos, dir)[0]

    def set_cost(pos: Position, dir: Direction, cost: int, tail: tuple[Position, ...]):
        key = visited_key(pos, dir)
        _cost_cache[key] = (cost, tail)

    def get_neighbours(pos: Position, dir: Direction) -> tuple[tuple[Position, Direction, int], ...]:
        result: list[tuple[Position, Direction, int]] = []

        orthonognal_dir: tuple[Literal[0, 1], Literal[0, 1]]

        if dir[0] != 0:
            orthonognal_dir = (0, 1)
        else:
            orthonognal_dir = (1, 0)

        cost = 0
        for _ in range(3):
            result.append((pos, orthonognal_dir, cost))
            pos = add_dir(pos, dir)
            cost += get_field_cost(pos)
            if not valid_pos(pos):
                break

        return tuple(r for r in result if r[2] < INFINITY)

    def navigate() -> int:
        visited: set[tuple[Position, Direction]] = set()
        queue: list[tuple[Position, Direction]] = [
            ((1, 0), (1, 0)),
            ((0, 1), (0, 1))
        ]
        count = 0
        while queue:
            count += 1
            queue.sort(key=lambda qe: get_cost(qe[0], qe[1]))
            pos, dir = queue.pop(0)
            pos_cost, tail = get_cost_tail(pos, dir)

            neighbours = tuple(
                n
                for n in get_neighbours(pos, dir)
                if visited_key(n[0], n[1]) not in visited
            )

            # visited.add(visited_key(pos, dir))

            # print("----", pos, dir, pos_cost)
            for p, nd, p_cost in neighbours:
                # print(p, nd, p_cost)
                p_cost += pos_cost
                # if p == dest:
                #    return p_cost
                for _dir in (nd, (-nd[0], -nd[1])):
                    _p = add_dir(p, _dir)
                    _p_cost = p_cost + get_field_cost(_p)
                    if _p_cost >= INFINITY:
                        continue
                    if _p_cost < get_cost(_p, nd):
                        set_cost(_p, nd, _p_cost, (*tail, _p))
                        if (_p, _dir) not in queue:
                            queue.append((_p, _dir))
                    # if _p == dest:
                    #    return _p_cost

            if count <= end_count:
                print("pos/dir/cost", pos, dir, pos_cost)
                print("neighbours", neighbours)
                print("queue", queue)
                print_costs()
                if count == end_count:
                    exit()

        last_tails = (get_cost_tail(dest, dir)
                      for pos, dir in _cost_cache if pos == dest)
        return min(ct[0] for ct in last_tails)

    end_count = -1

    def print_costs():
        def _format(pos: Position):
            return '/'.join(
                (
                    '{0:4d}'.format(_cost_cache[(pos, dir)][0])
                    if (pos, dir) in _cost_cache
                    else 'XXXX'
                )
                for dir in (
                    ((1, 0), (-1, 0), (0, 1), (0, -1),)
                    if ALL_DIRECTIONS
                    else ((1, 0), (0, 1),)
                )
            )

        for l, line in enumerate(field):

            print(' '.join((
                _format((i, l))
            ) for i, _ in enumerate(line)))

    result = navigate()
    # print_costs()
    # print("***********************")
    # print(get_cost_tail(dest, (1, 0)))
    # print(get_cost_tail(dest, (0, 1)))
    # print(_cost_cache)

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
