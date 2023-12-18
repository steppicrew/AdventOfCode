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
    field: list[list[bool]]

    def add_dir(pos: tuple[int, int], dir: tuple[int, int]) -> tuple[int, int]:
        return (pos[0] + dir[0], pos[1] + dir[1])

    def print_field():
        with open(file=path/("field" + part + EXT), mode="w", encoding='utf-8') as file:
            for line in field:
                file.write(''.join(('#' if c else '.') for c in line) + "\n")

    pos_dirs: list[tuple[tuple[int, int], tuple[int, int], int]] = []
    pos: tuple[int, int] = (0, 0)

    for input in inputs:
        dir, count, _color = input.split(' ')
        count = int(count)
        if dir == 'R':
            pos_dirs.append((pos, (1, 0), count))
            pos = (pos[0] + count, pos[1])
        elif dir == "L":
            pos_dirs.append((pos, (-1, 0), count))
            pos = (pos[0] - count, pos[1])
        elif dir == 'U':
            pos_dirs.append((pos, (0, -1), count))
            pos = (pos[0], pos[1] - count)
        elif dir == 'D':
            pos_dirs.append((pos, (0, 1), count))
            pos = (pos[0], pos[1] + count)

    toggle_fields: set[tuple[int, int]] = set()

    for i, pos_dir in enumerate(pos_dirs):
        if pos_dir[1][1] != 0:
            last_pos_dir_dir = pos_dirs[i - 2][1][1]
            last_pos_dir = pos_dirs[i-1]
            if last_pos_dir_dir == pos_dir[1][1]:
                # print(i, pos_dir, last_pos_dir)
                toggle_fields.add(
                    (max(pos_dir[0][0], last_pos_dir[0][0]), pos_dir[0][1]))

    min_x = min(p[0][0] for p in pos_dirs)
    max_x = max(p[0][0] for p in pos_dirs)
    min_y = min(p[0][1] for p in pos_dirs)
    max_y = max(p[0][1] for p in pos_dirs)

    field = [
        [False for _ in range(max_x - min_x + 1)]
        for _ in range(max_y - min_y + 1)
    ]
    field[-min_y][-min_x] = True

    for pos_dir in pos_dirs:
        pos = (pos_dir[0][0]-min_x, pos_dir[0][1] - min_y)
        for x in range(pos_dir[2] + 1):
            field[pos[1]][pos[0]] = True
            pos = add_dir(pos, pos_dir[1])

    print_field()

    for y, line in enumerate(field):
        inside: bool = False
        for x, cell in enumerate(line):
            if cell:
                result += 1
                xy = (x + min_x, y + min_y)
                if xy in toggle_fields:
                    inside = not inside
                elif x == 0 and not line[x+1]:
                    inside = not inside
                elif x < len(line) - 1 and not (line[x-1] or line[x+1]):
                    inside = not inside

            else:
                if inside:
                    result += 1
        # print(y, result)

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
