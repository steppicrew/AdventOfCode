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

    seeds = [int(s) for s in re.findall(r'\d+', inputs[0].split(':')[1])]

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

    def _map(value: int, maps: list[tuple[int, int, int]]) -> int:
        for m in maps:
            if value >= m[1] and value < m[1] + m[2]:
                return value - m[1] + m[0]
        return value

    locations: dict[int, int] = {}

    for seed in seeds:
        source = 'seed'
        value = seed
        while True:
            if source == 'location':
                locations[seed] = value
                break

            value = _map(value, maps[source][1])
            source = maps[source][0]

    result = min(locations.values())

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
