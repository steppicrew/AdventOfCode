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

    translate: dict[str, str] = {
        'one': "1",
        'two': "2",
        'three': "3",
        'four': "4",
        'five': "5",
        'six': "6",
        'seven': "7",
        'eight': "8",
        'nine': "9",
        'zero': "0",
    }

    numbers_re = r'\d|' + '|'.join(translate)
    reverse_numbers_re = r'\d|' + '|'.join(key[::-1] for key in translate)

    for input in inputs:  # pylint: disable=[redefined-builtin]
        match = re.findall(numbers_re, input)
        first_match = match[0]
        match = re.findall(reverse_numbers_re, input[::-1])
        last_match = match[0][::-1]
        if first_match in translate:
            first_match = translate[first_match]
        if last_match in translate:
            last_match = translate[last_match]
        number = int(first_match + last_match)
        result += number

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
