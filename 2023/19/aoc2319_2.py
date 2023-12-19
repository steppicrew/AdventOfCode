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


def print_off(*args):  # pylint: disable=unused-argument
    pass


debug = print_off


def run() -> int:
    result: int = 0

    workflows: dict[str, tuple[tuple[str, ...], ...]] = {}

    Item = tuple[
        tuple[int, int], tuple[int, int],
        tuple[int, int], tuple[int, int],
    ]

    accepted_items: list[Item] = []

    for input in inputs:
        if match := re.match(r'(\w+)\{(.+)\}', input):
            workflows[match[1]] = tuple(
                tuple(c.split(':', 1))
                for c in match[2].split(','))

    item: Item = (
        (1, 4000),
        (1, 4000),
        (1, 4000),
        (1, 4000),
    )

    def split_item(item: Item, property: int, value: int) -> tuple[Item | None, Item | None]:
        v = item[property]
        if v[1] <= value:
            return (item, None)
        if v[0] > value:
            return (None, item)

        item1: Item = item[:property] + \
            ((v[0], value),) + item[property+1:]  # type:ignore
        item2: Item = item[:property] + \
            ((value + 1, v[1]),) + item[property+1:]  # type:ignore
        return (item1, item2)

    queue: list[tuple[Item, str]] = [(item, 'in')]

    while queue:
        item, name = queue.pop(0)

        if name == 'A':
            debug("accepted", item)
            accepted_items.append(item)
        if name not in workflows:
            continue
        workflow = workflows[name]
        for conditions in workflow:
            if len(conditions) == 1:
                queue.append((item, conditions[0]))
                break
            field, operator, value = re.split(r'([<>])', conditions[0])
            value = int(value)
            if operator == '<':
                value -= 1
            item1, item2 = split_item(item, 'xmas'.index(field), value)
            if operator == '<':
                success_item = item1
                fail_item = item2
            else:
                fail_item = item1
                success_item = item2

            debug("split", name, conditions, success_item, fail_item)
            if success_item is not None:
                queue.append((success_item, conditions[1]))
            if fail_item is None:
                break
            item = fail_item

    for item in accepted_items:
        debug(item)

    for item in set(accepted_items):
        r = 1
        for _range in item:
            r *= _range[1] - _range[0] + 1
        debug(r, item)
        result += r

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
