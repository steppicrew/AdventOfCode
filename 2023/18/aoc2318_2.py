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

    pos_dirs: list[tuple[tuple[int, int], tuple[int, int], int]] = []
    pos: tuple[int, int] = (0, 0)

    for input in inputs:
        _dir, _count, color = input.split(' ')
        match = re.match(r'\(#([\da-f]{5})(\d)\)', color)
        if match is None:
            continue
        count = int(match.group(1), 16)
        dir = match.group(2)
        if dir == '0':
            pos_dirs.append((pos, (1, 0), count))
            pos = (pos[0] + count, pos[1])
        elif dir == '2':
            pos_dirs.append((pos, (-1, 0), count))
            pos = (pos[0] - count, pos[1])
        elif dir == '3':
            pos_dirs.append((pos, (0, -1), count))
            pos = (pos[0], pos[1] - count)
        elif dir == '1':
            pos_dirs.append((pos, (0, 1), count))
            pos = (pos[0], pos[1] + count)

    positions = [pd[0] for pd in pos_dirs]
    positions.sort(key=lambda pd: (pd[1], pd[0]))

    # print("positions", positions)

    def process_line(current_line: list[int], line_no: int, last_line_no: int | None, last_blocks: list[tuple[int, int]]) -> list[tuple[int, int]]:
        nonlocal result

        # print("*** process", current_line, line_no, last_line_no, last_blocks)

        count = sum(block[1] - block[0] + 1 for block in last_blocks)
        number_of_lines = line_no - last_line_no if last_line_no is not None else 1
        result += count * number_of_lines
        # print(
        #     'count', last_line_no, line_no,
        #     last_blocks, count, number_of_lines, result
        # )

        last_line = set((
            *[lb[0] for lb in last_blocks],
            *[lb[1] for lb in last_blocks],
        ))
        this_line_breaks = list(last_line)

        starts: list[int] = []
        ends: list[int] = []
        start: int | None = None
        for x in current_line:
            if start is None:
                start = x
            else:
                starts.append(start)
                ends.append(x)
                start = None
            this_line_breaks.append(x)

        this_line_breaks = [*set(this_line_breaks)]
        this_line_breaks.sort()

        # print("last_line", last_line)
        # print("this_line", this_line_breaks, starts, ends)

        had_start_in_last_line: bool = False
        next_blocks: list[tuple[int, int]] = []

        def add_block(start: int, end: int):
            if next_blocks and next_blocks[-1][1] == start:
                next_blocks[-1] = (next_blocks[-1][0], end)
            else:
                next_blocks.append((start, end))

        start: int | None = None
        last_start: int | None = None
        for x in this_line_breaks:
            # print("x1", x, start is not None)
            if x in starts:
                assert last_start is None
                # print("start", x)
                had_start_in_last_line = x in last_line
                if start is not None:
                    add_block(start, x)
                last_start = x
            elif x in ends:
                assert last_start is not None
                # print("end", x)
                had_end_in_last_line = x in last_line

                if had_start_in_last_line and had_end_in_last_line:
                    # both go up: remove from blocks
                    # print("both go up", start, last_start, x)
                    if start is not None:
                        add_block(last_start, x)
                        start = x
                        # print("add4", start, last_start, x, x-last_start + 1)
                        result += x - last_start - 1

                elif not had_start_in_last_line and not had_end_in_last_line:
                    # both got down: add to blocks
                    # print("both go down", start, last_start, x)
                    if start is not None:
                        start = x
                    else:
                        add_block(last_start, x)
                        start = None
                        # print("add3", start, last_start, x, x-last_start + 1)
                        result += x - last_start + 1

                elif had_start_in_last_line:
                    # print("had only start up", start, last_start, x)
                    if start is not None:
                        add_block(last_start, x)
                        start = None
                        # print("add1", start, last_start, x, x-last_start)
                        result += x - last_start
                    else:
                        start = x

                else:
                    # print("had only end up", start, last_start, x)
                    if start is None:
                        start = last_start
                        # print("add2", start, last_start, x, x-last_start)
                        result += x - last_start
                    else:
                        start = None

                last_start = None
            else:
                if start is None:
                    start = x
                else:
                    add_block(start, x)
                    start = None

            # print("x2", x, start is not None)
            # if x in last_line:
            #    this_line_breaks.remove(x)

        # print("next_blocks", line_no, next_blocks)
        return next_blocks

    last_line_no = None
    current_line: list[int] = []
    current_line_no: int = positions[0][1]
    last_blocks: list[tuple[int, int]] = []
    count = 0
    line = 0
    for position in positions:
        if position[1] != current_line_no:
            last_blocks = process_line(
                current_line,
                current_line_no,
                last_line_no,
                last_blocks
            )
            current_line = [position[0]]
            if last_line_no is not None:
                line += current_line_no - last_line_no
            last_line_no, current_line_no = current_line_no, position[1]
            count += 1
            # print(line, last_blocks, result)
            if line == -37:
                exit()
        else:
            current_line.append(position[0])

    last_blocks = process_line(current_line, current_line_no,
                               last_line_no, last_blocks)
    # print(count, last_blocks, result)

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
