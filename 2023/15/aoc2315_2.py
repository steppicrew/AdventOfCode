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

    values = inputs[0].split(',')

    def get_hash(value: str):
        _hash = 0
        for c in value:
            _hash = ((_hash + ord(c)) * 17) & 0xFF
        return _hash

    boxes: tuple[list[tuple[str, int]], ...] = tuple(
        [] for _ in range(256)
    )

    for value in values:
        label, operator, focus = re.split(r'([\-=])', value)
        box = boxes[get_hash(label)]
        lens_index: int | None = (
            [i for i, lens in enumerate(box) if lens[0] == label] or [None]
        )[0]

        if operator == '-':
            if lens_index is not None:
                box.pop(lens_index)
        else:
            lens = (label, int(focus))
            if lens_index is None:
                box.append(lens)
            else:
                box[lens_index] = lens

    for box_index, box in enumerate(boxes):
        for lens_index, lens in enumerate(box):
            result += (box_index+1) * (lens_index+1) * lens[1]

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
