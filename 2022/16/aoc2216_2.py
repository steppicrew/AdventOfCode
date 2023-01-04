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
                    sorted(
                        (v, data[v][0]) for v in visited if valves[v][0] > 0
                    )
                )
                break

        return _distance_cache[start]

    for input in inputs:
        if match := re.match(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)', input):
            valves[match[1]] = (int(match[2]), tuple(
                dest for dest in match[3].split(', ')))

    i = 0

    checked_ways: set[str] = set()

    def explore_branch(start_me: str, wait_me, start_el: str, wait_el: int, time_left: int, open_valves: set[str], way_me: list[Tuple[int, str]], way_el: list[Tuple[int, str]]) -> Tuple[int, list[Tuple[int, str]], list[Tuple[int, str]], set[str]]:
        nonlocal i
        i += 1
        _i = i
        if i % 1_000_000 == 0:
            print("Iteration", i / 1_000_000, "Mio")
        if i > 1_000_000_000:
            print("ABORT!")
            return (0, way_me, way_el, open_valves)

        min_wait = min(wait_me, wait_el)
        time_left -= min_wait
        wait_me -= min_wait
        wait_el -= min_wait

        '''
        print(
            f"*********** {_i}:{time_left}: start_me: {start_me}, wait_me: {wait_me}, start_el: {start_el}, wait_el: {wait_el}"
        )
        print("Me:", way_me)
        print("El:", way_el)
        '''

        def get_check_way(way_me: list[Tuple[int, str]], way_el: list[Tuple[int, str]]) -> str:
            return ' '.join(sorted(('-'.join(w[1] for w in way_me), '-'.join(w[1] for w in way_el))))

        def next_explore_me(new_start: str, new_dist: int):
            open_wait = 1 if start in open_valves else 0
            '''
            print(
                f"Me: from {start} to {new_start} in {new_dist} + {open_wait}")
            '''
            new_way = way_me + [(new_dist, new_start)]
            check_way = get_check_way(new_way, way_el)
            if check_way in checked_ways:
                return (0, way_me, way_el, open_valves)
            best_branch = explore_branch(
                new_start, new_dist + open_wait, start_el, wait_el, time_left, open_valves, new_way, way_el)
            checked_ways.add(check_way)
            return (valves[start][0] * (time_left - open_wait) + best_branch[0], best_branch[1], best_branch[2], best_branch[3])

        def next_explore_el(new_start: str, new_dist: int):
            open_wait = 1 if start in open_valves else 0
            '''
            print(
                f"El: from {start} to {new_start} in {new_dist} + {open_wait}")
            '''
            new_way = way_el + [(new_dist, new_start)]
            check_way = get_check_way(way_me, new_way)
            if check_way in checked_ways:
                return (0, way_me, way_el, open_valves)
            best_branch = explore_branch(
                start_me, wait_me, new_start, new_dist + open_wait, time_left, open_valves, way_me, new_way)
            checked_ways.add(check_way)
            return (valves[start][0] * (time_left - open_wait) + best_branch[0], best_branch[1], best_branch[2], best_branch[3])

        ident: str
        start: str
        next_explore: Callable[[str, int],
                               Tuple[int, list[Tuple[int, str]], list[Tuple[int, str]], set[str]]]

        if wait_me == 0:
            ident = "me"
            start = start_me
            next_explore = next_explore_me
        else:
            ident = "el"
            start = start_el
            next_explore = next_explore_el

        if start in open_valves:
            # print(f"********** Already open {start}")
            return (0, way_me, way_el, open_valves)

        open_valves = set(open_valves)
        if valves[start][0]:
            open_valves.add(start)
        distances = tuple(
            d for d in get_distances(start) if d[0] not in open_valves and d[1] < time_left
        )

        if not distances:
            return next_explore(start, time_left)

        max_value = max(
            (next_explore(next_valve, dist) for next_valve, dist in distances),
            key=lambda v: v[0]
        )

        # print(f"#### {_i} {ident} ({time_left}) max_value: {max_value}")
        # print(f"me: {start_me}, {wait_me}, {way_me}")
        # print(f"el: {start_el}, {wait_el}, {way_el}")

        return max_value

    result = explore_branch('AA', 0, 'AA', 0, 26, set(), [], [])
    print("Iterations:", i)
    # print(checked_ways)
    print(result)

    return result[0]


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
