# https://adventofcode.com/2022/day/18
from pathlib import Path
from functools import reduce
import re
from typing import Callable, Tuple
import json

ref = 1
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():
    result = 0

    room: list[list[bool]] = []
    room_width: int = 7
    stones: list[list[list[bool]]] = [
        # 1 -
        [
            [True, True, True, True],
        ],
        # 2 +
        [
            [False, True, False],
            [True, True, True],
            [False, True, False],
        ],
        # 3 J
        [
            [True, True, True],
            [False, False, True],
            [False, False, True],
        ],
        # 4 I
        [
            [True],
            [True],
            [True],
            [True],
        ],
        # 5 o
        [
            [True, True],
            [True, True],
        ]
    ]
    jets: Tuple[bool] = tuple(
        c == '>' for c in inputs[0]
    )
    jet_count = len(jets)

    def place_stone(stone: list[list[bool]], x: int, y: int, place: bool = False) -> bool:
        width = len(stone[0])
        if y < 0 or x < 0 or x + width - 1 >= room_width:
            return False
        for _y, row in enumerate(stone):
            if y + _y >= len(room):
                if place:
                    room.append([False for _ in range(room_width)])
                else:
                    return True

            for _x, part in enumerate(row):
                if part:
                    if place:
                        room[y + _y][x + _x] = True
                    elif room[y + _y][x + _x]:
                        return False
        return True

    def print_room():
        for line in reversed(room):
            print(''.join('#' if s else '.' for s in line))

    jet_index = 0
    for stone_number in range(2022):
        stone = stones[stone_number % len(stones)]
        x, y = 2, len(room) + 3
        while True:
            jet = jets[jet_index % jet_count]
            jet_index += 1
            try_x = x + (1 if jet else -1)
            if place_stone(stone, try_x, y):
                x = try_x
            if place_stone(stone, x, y - 1):
                y -= 1
            else:
                place_stone(stone, x, y, True)
                break
            if stone_number == 2:
                print('right' if jet else 'left', x, y)
        if stone_number == 2:
            print_room()

    result = len(room)

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
