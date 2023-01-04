# https://adventofcode.com/2022/day/17
from pathlib import Path
from functools import reduce
import re
from typing import Callable, NamedTuple, Tuple
import json

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---

"""
Verfahren: Finde die erste Wiederholung.
Vervielfältige den wiederholten Abschnitt und gehe vom letzmöglichen Zeitpunkz weiter
"""


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
    stone_count = len(stones)
    jets: Tuple[bool] = tuple(
        c == '>' for c in inputs[0]
    )
    jet_count = len(jets)

    removed_rows = 0
    removed_rows_0 = 0

    def place_stone(stone: list[list[bool]], x: int, y: int, place: bool = False) -> bool:
        nonlocal removed_rows, room

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
        if place:
            max_rows = [0 for _ in room[0]]
            for col in range(len(room[0])):
                for row in range(len(room)):
                    if room[row][col]:
                        max_rows[col] = row + 1

            remove = min(max_rows)
            if remove:
                removed_rows += remove
                room = room[remove:]
        return True

    def print_room():
        for line in reversed(room):
            print(''.join('#' if s else '.' for s in line))

    def drop_stone(stone_index: int, jet_index: int) -> int:
        stone = stones[stone_index]
        x, y = 2, len(room) + 3

        while True:
            jet = jets[jet_index]
            jet_index += 1
            if jet_index == jet_count:
                jet_index = 0

            try_x = x + (1 if jet else -1)
            if place_stone(stone, try_x, y):
                x = try_x
            if place_stone(stone, x, y - 1):
                y -= 1
            else:
                place_stone(stone, x, y, True)
                return jet_index

    jet_index = 0
    jet_stone_rooms: dict[tuple[int, int, str], tuple[int, int]] = dict()
    MAX = 1_000_000_000_000
    # MAX = 2022

    class RepeatValue(NamedTuple):
        last_stone_no: int
        last_removed_rows: int
        this_stone_no: int
        this_removed_rows: int
        jet_index: int
        room_height: int

    repeat_values: RepeatValue | None = None

    # Find first repitition
    for stone_no in range(MAX):
        stone_index = stone_no % stone_count
        jet_stone_room = (jet_index, stone_index, "|".join(
            ''.join('#' if s else '.' for s in line) for line in room))
        if jet_stone_room in jet_stone_rooms:
            repeat_values = RepeatValue(
                last_stone_no=jet_stone_rooms[jet_stone_room][0],
                last_removed_rows=jet_stone_rooms[jet_stone_room][1],
                this_stone_no=stone_no,
                this_removed_rows=removed_rows,
                jet_index=jet_index,
                room_height=len(room),
            )
            print("Wiederholung!", repeat_values, jet_stone_room)
            print("removed rows", removed_rows)
            break
        else:
            jet_stone_rooms[jet_stone_room] = (stone_no, removed_rows)

        jet_index = drop_stone(stone_index=stone_index, jet_index=jet_index)

    # Setze kurz vor Ende fort und extrapoliere die übersprungenen enfernten Zeilen
    if repeat_values:
        stone_diff = repeat_values.this_stone_no - repeat_values.last_stone_no
        removed_rows_diff = repeat_values.this_removed_rows - \
            repeat_values.last_removed_rows

        skip = (MAX-repeat_values.last_stone_no) // stone_diff
        removed_rows_0 = removed_rows_diff * skip + repeat_values.last_removed_rows

        print("Starting at", stone_diff * skip + repeat_values.last_stone_no)
        print(f"Skipping {skip}*{stone_diff} + {repeat_values.last_stone_no}")

        removed_rows = 0
        for stone_no in range(stone_diff * skip + repeat_values.last_stone_no, MAX):
            stone_index = stone_no % stone_count

            jet_index = drop_stone(
                stone_index=stone_index, jet_index=jet_index)

    result = removed_rows_0 + removed_rows + len(room)
    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
