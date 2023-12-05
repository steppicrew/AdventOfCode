# https://adventofcode.com/2022/day/18
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

    room: dict[tuple[int, int, int], int] = dict()

    max_x = max_y = max_z = 0

    XM = 1 << 0
    XP = 1 << 1
    YM = 1 << 2
    YP = 1 << 3
    ZM = 1 << 4
    ZP = 1 << 5

    '''
    directions2 = {
        XM: (
            (((-1, -1, 0), YP), ((0, -1, 0), XM), ((0, 0, 0), YM)),
            (((-1, 0, -1), ZP), ((0, 0, -1), XM), ((0, 0, 0), ZM)),
            (((-1,  1, 0), YM), ((0, 1,  0), XM), ((0, 0, 0), YP)),
            (((-1, 0,  1), ZM), ((0, 0,  1), XM), ((0, 0, 0), ZP)),
        ),
        XP: (
            (((1, -1, 0), YP), ((0, -1, 0), XP), ((0, 0, 0), YM)),
            (((1, 0, -1), ZP), ((0, 0, -1), XP), ((0, 0, 0), ZM)),
            (((1,  1, 0), YM), ((0, 1,  0), XP), ((0, 0, 0), YP)),
            (((1, 0,  1), ZM), ((0, 0,  1), XP), ((0, 0, 0), ZP)),
        ),
    }
    '''

    dir_face_map = {
        XM: ((-1, 0, 0), (), (-1, 1), (-1, 1)),
        XP: ((1, 0, 0), (), (-1, 1), (-1, 1)),
        YM: ((0, -1, 0), (-1, 1), (), (-1, 1)),
        YP: ((0, 1, 0), (-1, 1), (), (-1, 1)),
        ZM: ((0, 0, -1), (-1, 1), (-1, 1), ()),
        ZP: ((0, 0, 1), (-1, 1), (-1, 1), ()),
    }
    directions: dict[int, list[tuple[tuple[tuple[int, int, int], int],
                                     tuple[tuple[int, int, int], int], tuple[tuple[int, int, int], int]]]] = {}
    for dir_face, values in dir_face_map.items():
        directions[dir_face] = []
        sx, sy, sz = values[0]

        def get_face(x: int, y: int, z: int):
            if x == -1:
                return XP
            elif x == 1:
                return XM
            elif y == -1:
                return YP
            elif y == 1:
                return YM
            elif z == -1:
                return ZP
            elif z == 1:
                return ZM
            raise Exception("Something went wrong")

        def add(x: int, y: int, z: int):
            v1 = ((x + sx, y + sy, z + sz), get_face(x, y, z))
            v2 = ((x, y, z), dir_face)
            v3 = ((0, 0, 0), get_face(-x, -y, -z))
            directions[dir_face].append((v1, v2, v3))

        for x in values[1]:
            add(x, 0, 0)
        for y in values[2]:
            add(0, y, 0)
        for z in values[3]:
            add(0, 0, z)

    for input in inputs:
        x, y, z = [int(c) for c in input.split(',')]

        room[(x, y, z)] = 0b111111
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if z > max_z:
            max_z = z

    for x, y, z in room:
        for i, c in enumerate(((x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1))):
            if c in room:
                room[c] ^= 1 << i

    # find an outer stone
    outer_stone = None
    for x in range(max_x):
        for y in range(max_y):
            if (x, y, max_z) in room:
                outer_stone = (x, y, max_z)
                break

    seen_stone_faces: set[tuple[tuple[int, int, int], int]] = set()

    if outer_stone:
        stone_face_queue: set[tuple[tuple[int, int, int], int]] = set(
            ((outer_stone, ZP),))
        seen_stone_faces = set(stone_face_queue)
        while len(stone_face_queue):
            current_stone_face = stone_face_queue.pop()
            seen_stone_faces.add(current_stone_face)

            (x, y, z), current_face = current_stone_face
            for dir in directions[current_face]:
                for (dx, dy, dz), next_face in dir:
                    next_stone_face = ((x+dx, y+dy, z+dz), next_face)
                    # print("Checking", next_stone_face, current_stone_face)
                    if next_stone_face[0] in room:
                        # print("Match!")
                        if next_stone_face not in seen_stone_faces:
                            # print("Not in queue already")
                            stone_face_queue.add(next_stone_face)
                            seen_stone_faces.add(next_stone_face)
                        break

            print("queue length", len(stone_face_queue), len(seen_stone_faces))

    result = len(seen_stone_faces)
    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
