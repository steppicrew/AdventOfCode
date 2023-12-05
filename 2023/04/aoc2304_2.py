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
    # result: int = 0  # pylint: disable=[redefined-outer-name]

    cards: list[int] = []

    for input in inputs:  # pylint: disable=[redefined-builtin]
        _, remain = input.split(':')
        winning_str, owning_str = remain.split('|')

        winning = set(int(n) for n in re.findall(r'\d+', winning_str))
        win = 0
        for own in (int(n) for n in re.findall(r'\d+', owning_str)):
            if own in winning:
                win += 1
        cards.append(win)

    card_count = [1 for _ in cards]

    for i, win in enumerate(cards):
        for j in range(i+1, i + win + 1):
            card_count[j] += card_count[i]

    result = sum(card_count)

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
