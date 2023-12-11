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


def run() -> int:  # pylint: disable=[missing-function-docstring]
    result: int = 0  # pylint: disable=[redefined-outer-name]

    Direction = tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]]

    PipeDirections = tuple[
        Direction,
        Direction,
    ]
    Position = tuple[int, int]
    NO_PIPE = ((0, 0), (0, 0))

    s: Position = (0, 0)
    tiles: list[list[PipeDirections]] = []

    directions: dict[str, PipeDirections] = {
        '|': ((0, -1), (0, 1)),
        '-': ((-1, 0), (1, 0)),
        'L': ((0, -1), (1, 0)),
        'J': ((0, -1), (-1, 0)),
        '7': ((-1, 0), (0, 1)),
        'F': ((1, 0), (0, 1)),
        '.': NO_PIPE,
        'S': NO_PIPE,
    }

    start_corners: set[PipeDirections] = set((
        directions['L'], directions['F']
    ))
    end_corners: dict[PipeDirections, PipeDirections] = {
        directions['J']: directions['F'],
        directions['7']: directions['L'],
    }

    for input in inputs:  # pylint: disable=[redefined-builtin]
        tiles.append([directions[t] for t in input])
        if match := re.search('S', input):
            s = (match.start(), len(tiles) - 1)

    def pos_add(p: Position, _dir: Direction):
        return (p[0] + _dir[0], p[1] + _dir[1])

    def neighbour_matches(position: Position, *directions: Direction):
        def invert(_dir: Direction):
            return (-_dir[0], -_dir[1])

        def neighbour_has(p: Position, _dir: Direction):
            neighbour = pos_add(p, _dir)
            if neighbour[1] < 0 or neighbour[1] >= len(tiles):
                return False
            row = tiles[neighbour[1]]
            if neighbour[0] < 0 or neighbour[1] >= len(row):
                return False
            invert_dir = invert(_dir)
            return row[neighbour[0]][0] == invert_dir or row[neighbour[0]][1] == invert_dir

        return tuple(dir for dir in directions if neighbour_has(position, dir))

    s_neighbors = neighbour_matches(s, (-1, 0), (0, -1), (1, 0), (0, 1))
    tiles[s[1]][s[0]] = (s_neighbors[0], s_neighbors[1])

    pipe_positions: set[Position] = set((s,))
    p: Position = pos_add(s, s_neighbors[0])
    previous = s

    while p != s:
        pipe_positions.add(p)
        pipe = tiles[p[1]][p[0]]
        next_dir = pipe[1] if pos_add(p, pipe[0]) == previous else pipe[0]
        previous = p
        p = pos_add(p, next_dir)

    inside_tiles: set[Position] = set()
    last_corner = NO_PIPE
    for r, row in enumerate(tiles):
        inside: bool = False
        for c, tile in enumerate(row):
            if (c, r) not in pipe_positions:
                if inside:
                    inside_tiles.add((c, r))
            else:
                if tile == directions['|']:
                    inside = not inside
                elif tile in start_corners:
                    last_corner = tile
                elif tile in end_corners:
                    if last_corner == end_corners[tile]:
                        inside = not inside
                    last_corner = NO_PIPE

    result = len(inside_tiles)

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
