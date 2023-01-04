# https://adventofcode.com/2022/day/16
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

    valves: dict[str, Tuple[int, Tuple[str]]] = {}

    _distance_cache: dict[str, dict[str, Tuple[int, str]]] = {}

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

                _distance_cache[start] = {v: data[v] for v in visited}
                break

        return _distance_cache[start]

    for input in inputs:
        if match := re.match(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)', input):
            valves[match[1]] = (int(match[2]), tuple(
                dest for dest in match[3].split(', ')))

    max_time = 30
    time_left = max_time
    current_valve = 'AA'
    open_valves: set[str] = set()

    print(valves)

    while time_left > 0:
        time_left -= 1

        print("")
        print(f"== Minute {max_time - time_left} ==")

        if open_valves:
            pressure = sum(valves[v][0] for v in open_valves)
            print(
                f"Open valves {', '.join(sorted(open_valves))} releasing {pressure} pressure")
            result += pressure
        else:
            print("No valves are open")

        distances = get_distances(current_valve)
        next_valves = [
            (v, max(time_left - d[0], 0) * valves[v][0], d[0], valves[v][0])
            for v, d in distances.items()
            if valves[v][0] > 0 and v not in open_valves
        ]
        if not next_valves:
            continue
        next_valves.sort(key=lambda v: v[1])
        print(next_valves)
        best_valve = next_valves[-1]
        if best_valve[0] == current_valve:
            pressure = valves[current_valve][0]
            open_valves.add(current_valve)
            print(
                f"Open valve {current_valve}: pressure {pressure} for {time_left} minutes")
            continue

        current_valve = best_valve[0]
        while distances[current_valve][0] > 1:
            current_valve = distances[current_valve][1]

        print(
            f"Move to {current_valve} want to {best_valve[0]}")

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
