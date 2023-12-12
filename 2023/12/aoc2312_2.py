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

    cache: dict[tuple[str, str], int] = {}

    def count_matches(groups: list[str], stats: list[int]) -> int:
        key = ('.'.join(groups), ','.join(str(s) for s in stats))

        _cache = cache.get(key)
        if _cache is not None:
            return _cache

        def set_cache(value):
            cache[key] = value
            return value

        if not stats:
            return set_cache(
                1
                if ''.join(groups).find('#') < 0
                else 0
            )

        if not groups:
            return set_cache(0)

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
                    return set_cache(0)

        for start in range(0, range_max - stat + 1):
            if start + stat < len(group) and group[start + stat] == '#':
                continue
            count += count_matches(
                [
                    group[start + stat + 1:],
                    *groups[1:]
                ],
                stats[1:]
            )

        return set_cache(count)

    for input in inputs[:]:  # pylint: disable=[redefined-builtin]
        line, _stats = input.split(" ")
        line = re.sub(r'\.\.+', '.', line)
        full_line = '?'.join((line, line, line, line, line))
        full_stats = [
            int(s)
            for s in ','.join((_stats, _stats, _stats, _stats, _stats)).split(',')
        ]
        groups = full_line.split('.')

        cache.clear()
        count = count_matches(groups, full_stats)

        # print(groups, full_line, full_stats, count)
        result += count

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
