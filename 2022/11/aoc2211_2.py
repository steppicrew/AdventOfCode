# https://adventofcode.com/2022/day/11
from pathlib import Path
from functools import reduce
import re
from typing import Callable, Tuple

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():

    monkeys: list[Tuple[list[int], Callable[[int], int],
                        Callable[[int], bool], int, int]] = []

    def build_modify(operator: str, operand: str):
        if operator == '+':
            if operand == 'old':
                return lambda w: w + w
            else:
                return lambda w: w + int(operand)
        elif operator == '*':
            if operand == 'old':
                return lambda w: w * w
            else:
                return lambda w: w * int(operand)
        else:
            assert None

    def build_test(divider: int):
        return lambda w: w % divider == 0

    max_modulo = 1

    for input in inputs:
        if input.startswith('Monkey '):
            monkeys.append(([], lambda _: 0, lambda _: False, 0, 0))
        elif match := re.match(r' *Starting items: (\d+(?:, \d+)*)', input):
            monkeys[-1][0].extend(int(i) for i in match[1].split(", "))
        elif match := re.match(r' *Operation: new = old ([\*\+]) (\d+|old)', input):
            monkey = monkeys[-1]
            monkeys[-1] = (monkey[0], build_modify(match[1],
                           match[2]), monkey[2], monkey[3], monkey[4])
        elif match := re.match(r' *Test: divisible by (\d+)', input):
            monkey = monkeys[-1]
            monkeys[-1] = (monkey[0], monkey[1],
                           build_test(int(match[1])), monkey[3], monkey[4])
            max_modulo *= int(match[1])
        elif match := re.match(r' *If true: throw to monkey (\d+)', input):
            monkey = monkeys[-1]
            monkeys[-1] = (monkey[0], monkey[1],
                           monkey[2], int(match[1]), monkey[4])
        elif match := re.match(r' *If false: throw to monkey (\d+)', input):
            monkey = monkeys[-1]
            monkeys[-1] = (monkey[0], monkey[1],
                           monkey[2], monkey[3], int(match[1]))

    monkey_count = [0 for _ in range(len(monkeys))]

    for round in range(10_000):
        if round % 1000 == 0:
            print(round, monkey_count)
        for i, monkey in enumerate(monkeys):
            while monkey[0]:
                monkey_count[i] += 1
                item_worry = monkey[0].pop(0)
                item_worry = monkey[1](item_worry) % max_modulo
                # item_worry = int(item_worry/3)
                if monkey[2](item_worry):
                    monkeys[monkey[3]][0].append(item_worry)
                else:
                    monkeys[monkey[4]][0].append(item_worry)

    monkey_count.sort()
    result = monkey_count[-1] * monkey_count[-2]
    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
