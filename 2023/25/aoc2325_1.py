# https://adventofcode.com/2023/day/01
import re
from itertools import islice
from math import prod
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
debug_off = print_off


def run() -> int:
    result: int = 0

    neighbours: dict[str, set[str]] = {}

    for input in inputs:
        devices = re.findall(r'\w+', input)
        d1 = devices[0]
        if not d1 in neighbours:
            neighbours[d1] = set()
        for d2 in devices[1:]:
            if not d2 in neighbours:
                neighbours[d2] = set()
            neighbours[d1].add(d2)
            neighbours[d2].add(d1)

    def routing(start: str) -> dict[str, tuple[int, set[tuple[str, ...]]]]:
        costs: dict[str, tuple[int, set[tuple[str, ...]]]] = {
            d: (10_000, set())
            for d in neighbours
        }
        costs[start] = (0, set())
        queue: list[tuple[str, tuple[str, ...]]] = [(start, ())]
        visited: set[str] = set()
        while queue:
            queue.sort(key=lambda d: costs[d[0]][0])
            device, tail = queue.pop(0)
            if device in visited:
                continue
            visited. add(device)
            cost = costs[device][0] + 1
            tail = (*tail, device)
            for d in neighbours[device]:
                _cost = costs[d][0]
                if cost <= _cost:
                    if cost < _cost:
                        costs[d] = cost, set()
                    costs[d][1].add(tail + (d,))
                queue.append((d, tail))
        return costs

    def conn(d1: str, d2: str) -> tuple[str, str]:
        return (d2, d1) if d1 > d2 else (d1, d2)

    def analyze_connections(
        route_costs: dict[str, tuple[int, set[tuple[str, ...]]]],
        all_connections: dict[tuple[str, str], int]
    ):
        for _cost, tails in route_costs.values():
            for tail in tails:
                half_tail_len = (len(tail) - 1) // 2
                for i, d1 in enumerate(tail[:-1]):
                    c = conn(d1, tail[i+1])
                    value = half_tail_len - abs(i - half_tail_len)
                    if c == ("pzl", "rshx"):
                        print(c, i, value, len(tail))
                    if c not in all_connections:
                        all_connections[c] = value
                    else:
                        all_connections[c] += value

        # print(all_connections)

    start_device = [*neighbours.keys()][0]
    route_costs = routing(start_device)
    max_cost = max(c[0] for c in route_costs.values())
    remotest_devices = [d for d, c in route_costs.items() if c[0] == max_cost]
    debug("remotest_devices", remotest_devices)

    all_connections: dict[tuple[str, str], int] = {}
    for device in remotest_devices:
        route_costs = routing(device)
        debug_off(route_costs)
        analyze_connections(route_costs, all_connections)

    max_count = max(all_connections.values())
    connections = [*all_connections.keys()]
    connections.sort(key=lambda c: all_connections[c], reverse=True)
    debug("max_count", max_count)

    def split() -> tuple[int, int] | None:
        def _split(c1: tuple[str, str], c2: tuple[str, str], c3: tuple[str, str]) -> tuple[int, int]:
            forbidden_connections: set[tuple[str, str]] = set((c1, c2, c3))
            queue: set[str] = set((start_device,))
            visited: set[str] = set()
            while queue:
                device = queue.pop()
                visited.add(device)
                for d in neighbours[device]:
                    if conn(device, d) in forbidden_connections:
                        continue
                    if d not in visited:
                        queue.add(d)
            return (len(visited), len(neighbours) - len(visited))

        for i1, c1 in enumerate(connections):
            for i2, c2 in enumerate(islice(connections, i1 + 1, None)):
                for c3 in islice(connections, i1 + i2 + 2, None):
                    _result = _split(c1, c2, c3)
                    debug("_result", _result)
                    if _result[1] > 0:
                        return _result

    debug("Starting split...")
    _result = split()
    if _result is not None:
        result = prod(_result)
    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
