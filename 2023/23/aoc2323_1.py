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

    Coord = tuple[int, int]

    field = tuple(inputs)

    start = (inputs[0].find('.'), 0)
    end = (inputs[-1].find('.'), len(field)-1)

    queue: list[tuple[Coord, str, tuple[Coord, ...]]] = [
        (start, '.', (start,))]

    end_tails: list[tuple[Coord, ...]] = []

    def test_position(pos: Coord) -> str | None:
        if 0 <= pos[0] < len(field[0]) and 0 <= pos[1] < len(field):
            if field[pos[1]][pos[0]] != '#':
                return field[pos[1]][pos[0]]
        return None

    count = 0

    while queue:
        count += 1
        position, c, tail = queue.pop(0)
        # debug(position, c, tail, len(queue))
        if count == -17:
            debug(count, "queue", queue)
            exit()
        next_positions: tuple[Coord, ...]
        if c == '.':
            next_positions = (
                (position[0] + 1, position[1]),
                (position[0] - 1, position[1]),
                (position[0], position[1] + 1),
                (position[0], position[1] - 1),
            )
        elif c == '>':
            next_positions = ((position[0] + 1, position[1]),)
        elif c == '<':
            next_positions = ((position[0] - 1, position[1]),)
        elif c == 'v':
            next_positions = ((position[0], position[1] + 1),)
        else:
            debug(position, c)
            assert False

        for position in next_positions:
            # debug("test", position, tail)
            if position in tail:
                continue
            r = test_position(position)
            if r is None:
                continue
            queue.append((position, r, (*tail, position)))
            if position == end:
                end_tails.append((*tail, position))

    # debug(end_tails)

    result = max(len(t) for t in end_tails)

    return result - 1


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
