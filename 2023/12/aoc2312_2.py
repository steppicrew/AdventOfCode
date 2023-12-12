# https://adventofcode.com/2023/day/01
import re
from pathlib import Path
from typing import Tuple

from memoized import Memoized

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

    @Memoized
    def count_matches(groups: Tuple[str, ...], stats: Tuple[int, ...]) -> int:

        if not stats:
            return (
                1
                if ''.join(groups).find('#') < 0
                else 0
            )

        if not groups:
            return 0

        count = 0

        group = groups[0]
        stat = stats[0]
        first_fix = group.find('#')
        if first_fix < 0:
            count += count_matches(groups[1:], stats)
            range_max = len(group)
        else:
            range_max = min(len(group), first_fix + stat)
            if range_max < len(group):
                while group[range_max] == '#' and range_max >= 0:
                    range_max -= 1
                if range_max < 0:
                    return 0

        for start in range(0, range_max - stat + 1):
            if start + stat < len(group) and group[start + stat] == '#':
                continue
            count += count_matches(
                (
                    group[start + stat + 1:],
                    *groups[1:]
                ),
                stats[1:]
            )

        return count

    for input in inputs:  # pylint: disable=[redefined-builtin]
        line, _stats = input.split(" ")
        full_line = '?'.join(5 * (line,))
        full_stats = 5 * tuple(
            int(s)
            for s in _stats.split(',')
        )
        groups = tuple(re.split(r'\.+', full_line))

        count = count_matches(groups, full_stats)

        # print(groups, full_line, full_stats, count)
        result += count

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
