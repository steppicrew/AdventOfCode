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

    seed_ranges = [(int(seed_pair.split(' ')[0]), int(seed_pair.split(' ')[0]) + int(seed_pair.split(' ')[1]) - 1)
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
        maps[source][1].append((m[0] - m[1], m[1], m[1] + m[2]))

    def _map(values: list[tuple[int, int]], maps: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
        ranges: list[tuple[int, int]] = []
        values = list(values)
        maps = list(maps)
        values.sort(key=lambda v: v[0])
        maps.sort(key=lambda v: v[1])

        for v, v_end in values:

            for dest_offset, source_start, source_end in maps:
                while v < source_end and v <= v_end:
                    if v < source_start:
                        ranges.append((v, min(v_end, source_start - 1)))
                        v = source_start
                    else:
                        this_end = min(v_end, source_end - 1)
                        ranges.append((
                            max(v, source_start) + dest_offset,
                            this_end + dest_offset
                        ))
                        v = this_end+1

            if v < v_end:
                ranges.append((v, v_end))

        ranges.sort(key=lambda r: r[0])

        # clean up ranges
        _ranges: list[tuple[int, int]] = [ranges[0]]
        for r in ranges[1:]:
            if r[0] <= _ranges[-1][1] + 1:
                _ranges[-1] = (_ranges[-1][0], r[1])
            else:
                _ranges.append(r)

        return _ranges

    source = 'seed'
    value_ranges = seed_ranges
    while source != 'location':
        source, source_maps = maps[source]
        value_ranges = _map(value_ranges, source_maps)

    result = min(p[0] for p in value_ranges)

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
