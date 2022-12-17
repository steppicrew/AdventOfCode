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

    monkey_queue: list[list[int]] = []
    monkey_modify: list[Callable[[int], int]] = []
    monkey_test: list[Callable[[int], bool]] = []
    monkey_success_to: list[int] = []
    monkey_failed_to: list[int] = []

    monkey_count: list[int] = []

    mod_limit = 1

    def build_modify(operator: str, operand: str) -> Callable[[int], int]:
        def double(w: int) -> int: return w + w

        def square(
            w: int) -> int: return w * w
        if operator == '+':
            if operand == 'old':
                return double
            else:
                int_operand = int(operand)

                def add(w: int) -> int:
                    return w + int_operand
                return add
        elif operator == '*':
            if operand == 'old':
                return square
            else:
                int_operand = int(operand)

                def mul(w: int) -> int:
                    return w * int_operand
                return mul
        else:
            assert None

    def build_test(divider: int):
        nonlocal mod_limit
        mod_limit *= divider
        return lambda w: w % divider == 0

    for input in inputs:
        if input.startswith('Monkey '):
            monkey_count.append(0)
        elif match := re.match(r' *Starting items: (\d+(?:, \d+)*)', input):
            monkey_queue.append([int(i) for i in match[1].split(", ")])
        elif match := re.match(r' *Operation: new = old ([\*\+]) (\d+|old)', input):
            monkey_modify.append(build_modify(match[1], match[2]))
        elif match := re.match(r' *Test: divisible by (\d+)', input):
            monkey_test.append(build_test(int(match[1])))
        elif match := re.match(r' *If true: throw to monkey (\d+)', input):
            monkey_success_to.append(int(match[1]))
        elif match := re.match(r' *If false: throw to monkey (\d+)', input):
            monkey_failed_to.append(int(match[1]))

    for round in range(10_000):
        if round == 1 or round == 20 or round % 1000 == 0:
            print(round, monkey_count)
        for i in range(len(monkey_queue)):
            queue = monkey_queue[i]

            if not queue:
                continue

            modify = monkey_modify[i]
            test = monkey_test[i]
            success_queue = monkey_queue[monkey_success_to[i]]
            failed_queue = monkey_queue[monkey_failed_to[i]]
            # print(round, i, len(queue))
            monkey_count[i] += len(queue)
            monkey_queue[i] = []
            for item_worry in queue:
                item_worry = modify(item_worry) % mod_limit
                if test(item_worry):
                    success_queue.append(item_worry)
                else:
                    failed_queue.append(item_worry)
        # print([m[0] for m in monkeys])

    monkey_count.sort()
    result = monkey_count[-1] * monkey_count[-2]
    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
