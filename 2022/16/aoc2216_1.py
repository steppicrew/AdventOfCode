# https://adventofcode.com/2022/day/16
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

    valves: dict[str, Tuple[int, Tuple[str]]] = {}

    _distance_cache: dict[str, Tuple[Tuple[str, int]]] = {}

    def get_distances(start):
        if start not in _distance_cache:
            data: dict[str, Tuple[int, str]] = {start: (0, start)}
            visited: set[str] = set()
            current = start
            while True:
                visited.add(current)
                next_dist = data[current][0] + 1
                for candidate in (c for c in valves[current][1] if c not in visited):
                    if candidate not in data or data[candidate][0] < next_dist:
                        data[candidate] = (next_dist, current)

                best_candidates = sorted(
                    [c for c in data.keys() if c not in visited], key=lambda c: data[c][0])

                if best_candidates:
                    current = best_candidates[0]
                    continue

                _distance_cache[start] = tuple(
                    (v, data[v][0]) for v in visited if valves[v][0] > 0)
                break

        return _distance_cache[start]

    for input in inputs:
        if match := re.match(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)', input):
            valves[match[1]] = (int(match[2]), tuple(
                dest for dest in match[3].split(', ')))

    i = 0

    def explore_branch(start: str, time_left: int, open_valves: set[str], way: list[str]) -> int:
        nonlocal i
        i += 1
        if i > 100_000_000:
            return 0

        pressure = valves[start][0]
        if pressure:
            time_left -= 1

        result: int = pressure * time_left

        open_valves = set(open_valves)
        open_valves.add(start)
        way = way+[start]
        distances = tuple(d for d in get_distances(start)
                          if d[0] not in open_valves and d[1] < time_left)
        # print("Explore", start, time_left, way, distances)
        max_value = 0
        for next_valve, dist in distances:
            value = explore_branch(
                next_valve, time_left - dist, open_valves, way)
            if value > max_value:
                max_value = value

        return result + max_value

    result = explore_branch('AA', 30, set(), [])
    print(i)

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
