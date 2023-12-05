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

    max_draws: dict[str, int] = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    for input in inputs:  # pylint: disable=[redefined-builtin]
        if not input.strip():
            continue
        game, line = input.split(':', 1)
        draws = line.split(';')
        match = re.search(r'\d+', game)
        assert match is not None
        game_id = int(match.group(0))
        for draw in draws:
            for color_draw in draw.split(','):
                match = re.search(r'(\d+) (\w+)', color_draw)
                assert match is not None
                if max_draws[match.group(2)] < int(match.group(1)):
                    game_id = 0
        result += game_id

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
