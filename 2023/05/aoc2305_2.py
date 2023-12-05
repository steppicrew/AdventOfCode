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


def run() -> int:  # pylint: disable=[missing-function-docstring]
    result: int = 0  # pylint: disable=[redefined-outer-name]

    maps: dict[str, tuple[str, list[tuple[int, int, int]]]] = {}

    seeds = [(int(seed_pair.split(' ')[0]), int(seed_pair.split(' ')[0]) + int(seed_pair.split(' ')[1]) - 1)
             for seed_pair in re.findall(r'\d+\s+\d+', inputs[0].split(':')[1])]

    source: str = ''

    for input in inputs[1:]:  # pylint: disable=[redefined-builtin]
        if not input:
            continue
        if match := re.match(r'(\w+)-to-(\w+) map:', input):
            source = match.group(1)
            maps[source] = (match.group(2), [])
            continue

        if not source:
            continue

        m = tuple(int(n) for n in re.findall(r'\d+', input))
        maps[source][1].append((m[0], m[1], m[2]))

    def _map(values: list[tuple[int, int]], maps: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
        ranges: list[tuple[int, int]] = []
        values = list(values)
        maps = list(maps)
        values.sort(key=lambda v: v[0])
        maps.sort(key=lambda v: v[1])

        for v, v_end in values:

            for dest_start, source_start, length in maps:
                if v >= source_start + length:
                    continue

                if v < source_start:
                    ranges.append((v, min(v_end, source_start - 1)))
                    v = source_start

                if v > v_end:
                    break

                ranges.append((
                    max(v, source_start) - source_start + dest_start,
                    min(v_end, source_start + length - 1) -
                    source_start + dest_start
                ))
                v = min(v_end, source_start + length - 1)+1

                if v > v_end:
                    break

            if v < v_end:
                ranges.append((v, v_end))

        ranges.sort(key=lambda r: r[0])

        _ranges: list[tuple[int, int]] = [ranges[0]]

        for r in ranges[1:]:
            if r[0] <= _ranges[-1][1] + 1:
                _ranges[-1] = (_ranges[-1][0], r[1])
            else:
                _ranges.append(r)

        return _ranges

    locations: dict[tuple[int, int], list[tuple[int, int]]] = {}

    for seed in seeds:
        source = 'seed'
        value = [seed]
        while True:
            if source == 'location':
                locations[seed] = value
                break

            value = _map(value, maps[source][1])
            source = maps[source][0]

    result = min(p[0][0] for p in locations.values())

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
