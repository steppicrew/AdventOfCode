# https://adventofcode.com/2023/day/01
import re
from pathlib import Path
from typing import NamedTuple

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


class Item(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @property
    def value(self) -> int:
        return self.x + self.m + self.a + self.s

    def test(self, condition: str) -> bool:
        field, operator, value = re.split(r'([<>])', condition)
        value = int(value)

        def smaller(x: int):
            return x < value

        def larger(x: int):
            return x > value

        op_fn = smaller if operator == "<" else larger
        if field == 'x':
            return op_fn(self.x)
        if field == 'm':
            return op_fn(self.m)
        if field == 'a':
            return op_fn(self.a)
        if field == 's':
            return op_fn(self.s)
        return False


def run() -> int:
    result: int = 0

    workflows: dict[str, tuple[tuple[str, ...], ...]] = {}
    items: list[Item] = []

    for input in inputs:
        if match := re.match(r'(\w+)\{(.+)\}', input):
            workflows[match[1]] = tuple(
                tuple(c.split(':', 1))
                for c in match[2].split(','))
        if match := re.match(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}', input):
            items.append(Item(
                x=int(match[1]),
                m=int(match[2]),
                a=int(match[3]),
                s=int(match[4]),
            ))

    def set_workflow(name: str):
        nonlocal result
        workflow = workflows[name] if name in workflows else None
        if name == 'A':
            result += item.value
        return workflow

    for item in items:
        workflow: tuple[tuple[str, ...], ...] | None = workflows["in"]

        while workflow is not None:
            for conditions in workflow:
                if len(conditions) == 1:
                    workflow = set_workflow(conditions[0])
                    break

                if item.test(conditions[0]):
                    workflow = set_workflow(conditions[1])
                    break
    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
