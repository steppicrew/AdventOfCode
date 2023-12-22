# https://adventofcode.com/2023/day/01
import re
from itertools import islice
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


debug = print_off


def run() -> int:
    result: int = 0

    Coord = tuple[int, int, int]
    Brick = tuple[Coord, tuple[Coord, ...], int]

    bricks: list[Brick] = []

    for i, input in enumerate(inputs):
        match = re.match(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', input)
        if match:
            x_dim = (int(match[1]), int(match[4]))
            y_dim = (int(match[2]), int(match[5]))
            z_dim = (int(match[3]), int(match[6]))

            min_coords = (
                min(x_dim),
                min(y_dim),
                min(z_dim),
            )

            coords = tuple(
                (x - min_coords[0], y - min_coords[1], z - min_coords[2])
                for x in range(min_coords[0], max(x_dim) + 1)
                for y in range(min_coords[1], max(y_dim) + 1)
                for z in range(min_coords[2], max(z_dim) + 1)
            )

            bricks.append((min_coords, coords, i+1))

    bricks.sort(key=lambda b: (b[0][2], b[0][1], b[0][0]))

    fallen_bricks: list[Brick] = []
    occupied: set[Coord] = set()

    def space_is_used(occupied: set[Coord], brick: Brick, z: int) -> bool:
        x = brick[0][0]
        y = brick[0][1]
        for c in brick[1]:
            if (x + c[0], y + c[1], z + c[2]) in occupied:
                return True
        return False

    def add_brick(occupied: set[Coord], brick: Brick):
        x = brick[0][0]
        y = brick[0][1]
        z = brick[0][2]
        for c in brick[1]:
            occupied.add((x + c[0], y + c[1], z + c[2]))

    def remove_brick(occupied: set[Coord], brick: Brick):
        x = brick[0][0]
        y = brick[0][1]
        z = brick[0][2]
        for c in brick[1]:
            occupied.remove((x + c[0], y + c[1], z + c[2]))

    def drop_brick(occupied: set[Coord], brick: Brick) -> Brick:
        z = brick[0][2]

        # debug("starting", z, brick[2], len(brick[1]))
        while z > 1 and not space_is_used(occupied, brick, z-1):
            z -= 1
        # debug("ending", z, brick[2])
        return (
            (brick[0][0], brick[0][1], z),
            brick[1], brick[2]
        )

    for brick in bricks:
        dropped_brick = drop_brick(occupied, brick)
        fallen_bricks.append(dropped_brick)

        add_brick(occupied, dropped_brick)
        # debug(occupied)

    # for brick in fallen_bricks:
    #     debug(brick)
    # exit()

    for i, brick in enumerate(fallen_bricks):
        _occupied = set(occupied)
        remove_brick(_occupied, brick)
        fallen = 0
        for _brick in islice(fallen_bricks, i+1, None):
            if _brick[0][2] == brick[0][2]:
                continue
            remove_brick(_occupied, _brick)
            dropped_brick = drop_brick(_occupied, _brick)
            add_brick(_occupied, dropped_brick)
            if dropped_brick != _brick:
                fallen += 1

        if fallen > 0:
            debug("disintegrate", brick[2], fallen)
            result += fallen

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
