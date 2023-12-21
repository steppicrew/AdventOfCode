# https://adventofcode.com/2023/day/01
import re
from pathlib import Path
from typing import Callable

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
    start: Position | None = None

    for l, input in enumerate(inputs):
        start_index = input.find("S")
        if start_index >= 0:
            start = (l, start_index)
            break
    assert start is not None

    def test_from_start(start: Position, visited: dict[Position, int]):
        reached: list[Position] = [start]
        visited[start] = 0

        def add_if_reachable(x: int, y: int, list_to_add: list[Position], step: int) -> None:
            if (x, y) in visited:
                return
            if 0 <= x < len(field[0]) and 0 <= y < len(field):
                if field[y][x] != '#':
                    list_to_add.append((x, y))
                    visited[(x, y)] = step

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
        return visited

    def get_next_border(is_border_fn: Callable[[Position], bool]) -> tuple[int, tuple[Position, ...], int]:
        start_positions = (start,)
        count = 0
        while True:
            _visited: dict[Position, int] = {}
            next_map: dict[Position, int] | None = None
            for _start in start_positions:
                next_map = test_from_start(_start, _visited)

            assert next_map is not None

            min_next = min(
                v
                for p, v in next_map.items()
                if is_border_fn(p)
            )
            min_next_positions = tuple(
                p
                for p, v in next_map.items()
                if is_border_fn(p) and v == min_next
            )

            if min_next_positions == start_positions:
                return (count, min_next_positions, max(next_map.values()))

            start_positions = min_next_positions
            count += 1

    STEP = 3

    STEP_COUNT = 26501365

    if STEP == 1:
        debug("west", get_next_border(lambda p: p[0] == 0))
        debug("east", get_next_border(lambda p: p[0] == len(field[0])-1))
        debug("north", get_next_border(lambda p: p[1] == 0))
        debug("south", get_next_border(lambda p: p[1] == len(field)-1))
    elif STEP == 2:
        offset = start[0]
        width = len(field)
        full_radius = (STEP_COUNT - offset - 1) // width
        full_radius_mod = (STEP_COUNT - offset - 1) % width
        debug(full_radius)
    elif STEP == 3:
        offset = start[0]
        width = len(field)
        full_radius = (STEP_COUNT - offset - 1) // width
        full_radius_mod = (STEP_COUNT - offset - 1) % width

        def get_field_count(start: Position) -> tuple[tuple[int, int], dict[tuple[int, int], int]]:
            visited = test_from_start(start, {})

            # _odd = 1 - sum(start) % 2
            _odd = 1
            _even = 1 - _odd

            odd_field_count = len(tuple(
                v
                for v in visited.values()
                if v % 2 == _odd
            ))
            even_field_count = len(tuple(
                v
                for v in visited.values()
                if v % 2 == _even
            ))

            return ((even_field_count, odd_field_count), visited)

        field_counts: dict[str, tuple[tuple[int, int], dict[tuple[int, int], int]]] = {
            'middle-south': get_field_count((offset, 0)),
            'middle-north': get_field_count((offset, len(field) - 1)),
            'middle-west': get_field_count((len(field[0]) - 1, offset)),
            'middle-east': get_field_count((0, offset)),
            'north-east': get_field_count((0, len(field) - 1)),
            'north-west': get_field_count((len(field[0]) - 1, len(field) - 1)),
            'south-east': get_field_count((0, 0)),
            'south-west': get_field_count((len(field[0]) - 1, 0)),
        }
        # debug(field_counts)

        full_middle_field_count = field_counts["middle-east"][0]
        # debug("max middle", max(field_counts["middle-east"][1].values()))

        uni_filed = width % 2 == 0

        middle_index = STEP_COUNT % 2
        not_middle_index = middle_index if uni_filed else 1 - middle_index

        center_index = not_middle_index
        next_to_center_index = center_index if uni_filed else 1 - center_index
        alternate_index = next_to_center_index if uni_filed else 1 - next_to_center_index

        middle_outer_index = next_to_center_index if full_radius % 2 == 0 else alternate_index
        middle_not_outer_index = middle_outer_index if uni_filed else 1 - middle_outer_index

        corner_index = middle_outer_index if uni_filed or offset % 2 == 0 else 1 - \
            middle_outer_index
        next_corner_index = corner_index if uni_filed else 1 - corner_index

        corner_radius = full_radius_mod + offset
        next_corner_radius = full_radius_mod - offset - 1
        assert next_corner_radius == corner_radius - width

        count1 = (full_radius + 1) * (full_radius + 1)
        count2 = full_radius * full_radius

        # all full fields
        result = count1 * full_middle_field_count[middle_not_outer_index] + \
            count2 * full_middle_field_count[middle_outer_index]

        debug("center_index@start", center_index,
              field_counts["middle-east"][1][(offset, offset)], field_counts["middle-east"][1][(offset, offset)] % 2 == center_index)
        debug("center_index@right", center_index,
              field_counts["middle-east"][1][(len(field[0]) - 1, offset)], field_counts["middle-east"][1][(len(field[0]) - 1, offset)] % 2 == center_index)
        debug("next to center_index@left", next_to_center_index,
              field_counts["middle-east"][1][(0, offset)], field_counts["middle-east"][1][(0, offset)] % 2 == next_to_center_index)
        debug("next to center_index@right", next_to_center_index,
              field_counts["middle-east"][1][(len(field[0]) - 1, offset)], field_counts["middle-east"][1][(len(field[0]) - 1, offset)] % 2 == next_to_center_index)
        debug("next to next to center_index@left", alternate_index,
              field_counts["middle-east"][1][(0, offset)], field_counts["middle-east"][1][(0, offset)] % 2 == alternate_index)
        debug("middle_outer_index@left", middle_outer_index,
              field_counts["middle-east"][1][(0, offset)], field_counts["middle-east"][1][(0, offset)] % 2 == middle_outer_index)
        debug("middle_outer_index@(left, bottom)", middle_outer_index,
              field_counts["middle-east"][1][(0, len(field) - 1)], field_counts["middle-east"][1][(0, len(field) - 1)] % 2 == middle_outer_index)
        debug("below middle_outer_index@(0,0)", next_corner_index,
              field_counts["south-east"][1][(0, 0)], field_counts["south-east"][1][(0, 0)] % 2 == next_corner_index)
        debug("corner_index/next_corner_index",
              corner_index, next_corner_index)
        debug("full_radius", full_radius, full_radius_mod)
        debug("full_field_count odd", full_middle_field_count[1])
        debug("full_field_count even", full_middle_field_count[0])
        debug("max distance from corner", max(
            field_counts["south-east"][1].values()))
        debug("plants", sum(input.count('.') for input in inputs))

        north_count = len(
            [v for v, step in field_counts["middle-north"][1].items() if step <= full_radius_mod and step % 2 == middle_outer_index])
        south_count = len(
            [v for v, step in field_counts["middle-south"][1].items() if step <= full_radius_mod and step % 2 == middle_outer_index])
        east_count = len(
            [v for v, step in field_counts["middle-east"][1].items() if step <= full_radius_mod and step % 2 == middle_outer_index])
        west_count = len(
            [v for v, step in field_counts["middle-west"][1].items() if step <= full_radius_mod and step % 2 == middle_outer_index])

        north_east_count = len(
            [v for v, step in field_counts["north-east"][1].items() if step <= corner_radius and step % 2 == corner_index])
        north_west_count = len(
            [v for v, step in field_counts["north-west"][1].items() if step <= corner_radius and step % 2 == corner_index])
        south_east_count = len(
            [v for v, step in field_counts["south-east"][1].items() if step <= corner_radius and step % 2 == corner_index])
        south_west_count = len(
            [v for v, step in field_counts["south-west"][1].items() if step <= corner_radius and step % 2 == corner_index])

        next_north_east_count = len(
            [v for v, step in field_counts["north-east"][1].items() if step <= next_corner_radius and step % 2 == next_corner_index])
        next_north_west_count = len(
            [v for v, step in field_counts["north-west"][1].items() if step <= next_corner_radius and step % 2 == next_corner_index])
        next_south_east_count = len(
            [v for v, step in field_counts["south-east"][1].items() if step <= next_corner_radius and step % 2 == next_corner_index])
        next_south_west_count = len(
            [v for v, step in field_counts["south-west"][1].items() if step <= next_corner_radius and step % 2 == next_corner_index])

        result += north_count + east_count + west_count + south_count

        result += full_radius * \
            (north_east_count + north_west_count +
             south_east_count + south_west_count)

        result += (full_radius + 1) * \
            (next_north_east_count + next_north_west_count +
             next_south_east_count + next_south_west_count)

        debug(north_count, east_count, south_count, west_count)
        debug(north_east_count, north_west_count,
              south_east_count, south_west_count)
        debug(next_north_east_count, next_north_west_count,
              next_south_east_count, next_south_west_count)
        debug("corner radius", corner_radius, next_corner_radius)

        # 632251688988502 is too low
        # 632257939653947 is too low
        # 633251688996204 is too high
        # 632257949159150
        # 632257930142912
        # 632257949159150
        # 632257949361449
        # 632256778859435
        # 632257135306240
        # 632257153513195
        # 632257138745328
        # 632257138745283
        # 632257162212112

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
