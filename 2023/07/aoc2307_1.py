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

    card_values: dict[str, str] = {
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "T": "a",
        "J": "b",
        "Q": "c",
        "K": "d",
        "A": "e",
    }

    def get_deck_rank(deck: str):
        cards = list(deck)
        cards.sort()
        deck = ''.join(cards)
        counts: list[int] = []
        while deck:
            match = re.match(r'(.)\1*', deck)
            if match:
                cards = match.group()
                counts.append(len(cards))
                deck = deck[len(cards):]

        counts.sort(reverse=True)

        if counts[0] == 5 or counts[0] == 4:
            return counts[0] + 2
        if counts[0] == 3 and counts[1] == 2:
            return 5
        if counts[0] == 3:
            return 4
        if counts[0] == 2 and counts[1] == 2:
            return 3
        if counts[0] == 2:
            return 2
        return 1

    def get_deck_value(deck: str):
        return ''.join(card_values[c] for c in deck)

    decks: list[tuple[int, str, int]] = []
    for input in inputs:  # pylint: disable=[redefined-builtin]
        deck, bet = input.split(" ")
        decks.append((
            get_deck_rank(deck),
            get_deck_value(deck),
            int(bet)
        ))
    decks.sort(key=lambda deck: (deck[0], deck[1]))

    for deck in decks:
        print(deck)

    for i, deck in enumerate(decks):
        result += (i+1) * deck[2]

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
