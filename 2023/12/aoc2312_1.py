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

    def count_matches(groups: list[str], stats: list[int]) -> int:
        if not groups and not stats:
            return 1
        if not groups:
            return 0

        group = groups[0]

        if not stats:
            if ''.join(groups).find('#') >= 0:
                return 0
            return 1

        stat = stats[0]
        if len(group) < stat:
            if group.count('#') == 0:
                return count_matches(groups[1:], stats)
            else:
                return 0

        count = 0
        end = group.find('#')
        if end < 0:
            end = len(group) - stat
            count += count_matches(groups[1:], stats)
            # print("start count", count, groups[1:], stats)
        else:
            end = min(end, len(group) - stat)

        for i in range(end + 1):
            if i + stat < len(group) and group[i + stat] != '#':
                _next = count_matches(
                    [group[i+stat+1:], *groups[1:]], stats[1:])
                count += _next
            elif i + stat == len(group):
                _next = count_matches(groups[1:], stats[1:])
                count += _next

        return count

    for input in inputs[:]:  # pylint: disable=[redefined-builtin]
        line, _stats = input.split(" ")
        stats = [int(s) for s in _stats.split(',')]
        groups = re.findall(r'[\?#]+', line)
        count = count_matches(groups, stats)
        # print(line, stats, count)
        # exit()
        result += count if count is not None else 0

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
