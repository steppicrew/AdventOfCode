# https://adventofcode.com/2022/day/12
from pathlib import Path
from functools import reduce
import re

ref = 0
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():
    result = 0
    moving = False
    stacks: list[list[str]] = []
    for input in inputs:
        if not input:
            moving = True
            for stack in stacks:
                stack.pop()
            continue
        if moving:
            match = re.match(r'move (\d+) from (\d+) to (\d+)', input)
            assert match is not None
            count = int(match[1])
            f = int(match[2])-1
            t = int(match[3])-1
            chunk = stacks[f][:count]
            chunk.reverse()
            stacks[f] = stacks[f][count:]
            stacks[t] = chunk + stacks[t]
        else:
            i = 1
            while i < len(input):
                idx = int((i-1)/4)
                if len(stacks) <= idx:
                    stacks.append([])
                if input[i] != ' ':
                    stacks[idx].append(input[i])
                i += 4
    result = ''
    for stack in stacks:
        result += stack[0]
    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
