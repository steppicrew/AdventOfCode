# https://adventofcode.com/2022/day/15
from pathlib import Path
from functools import reduce
import re
from typing import Callable, Tuple
import json

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():
    result = 0

    def get_range_fn(s_x: int, s_y: int, dist: int):
        def range_fn(y: int):
            dy = abs(y - s_y)
            if dy > dist:
                return None
            return (s_x - (dist - dy), s_x + (dist - dy))
        return range_fn

    sensors: list[Callable[[int], tuple[int, int] | None]] = []
    beacons: dict[int, set[int]] = {}

    test_y = 10 if ref == 1 else 2000000

    for input in inputs:
        if match := re.match(r'Sensor at x=(\-?\d+), y=(\-?\d+): closest beacon is at x=(\-?\d+), y=(\-?\d+)', input):
            s_x, s_y, b_x, b_y = (int(i) for i in (
                match[1], match[2], match[3], match[4]))
            dist = abs(s_x - b_x) + abs(s_y - b_y)
            sensors.append(get_range_fn(s_x, s_y, dist))
            if b_y in beacons:
                beacons[b_y].add(b_x)
            else:
                beacons[b_y] = {b_x}

    '''
    for y in range(min_y, max_y + 1):
        print('%03d:' % y, ''. join(
            ('B' if (x, y) in beacons else '#' if (x, y) in seen else '.' for x in range(min_x, max_x + 1))))
    '''

    ranges: list[tuple[int, int]] = []
    found_y: int = 0
    for y in range(4_000_000):
        if y % 100_000 == 0:
            print("row", y)
        ranges = []
        for sensor in sensors:
            _range = sensor(y)
            if not _range:
                continue
            min_x, max_x = _range
            _ranges: list[tuple[int, int]] = []
            for _range in ranges:
                if min_x <= _range[1] and max_x >= _range[0]:
                    min_x = min(min_x, _range[0])
                    max_x = max(max_x, _range[1])
                else:
                    _ranges.append(_range)
            _ranges.append((min_x, max_x))
            ranges = _ranges
        if len(ranges) > 1:
            found_y = y
            break

    ranges.sort(key=lambda r: r[0])
    found_x = ranges[0][1] + 1
    result = found_x * 4_000_000 + found_y
    print(found_x, found_y, ranges)

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
