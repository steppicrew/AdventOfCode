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


debug = print


def run() -> int:
    result: int = 0

    Module = tuple[str, tuple[str, ...]]

    modules: dict[str, Module] = {}
    flipflip_states: dict[str, bool] = {}
    conjunction_states: dict[str, dict[str, bool]] = {}
    queue: list[tuple[str, str, bool]] = []
    broadcaster: Module = ("", ())

    high_count = 0
    low_count = 0

    for input in inputs:
        name, destinations = input.split(' -> ')
        if name == 'broadcaster':
            broadcaster = ('', tuple(destinations.split(', ')))
        else:
            modules[name[1:]] = (name[0], tuple(destinations.split(', ')))
            if name[0] == '%':
                flipflip_states[name[1:]] = False
            else:
                conjunction_states[name[1:]] = {}

    for con_name, con_state in conjunction_states.items():
        for source_name, module in modules.items():
            if con_name in module[1]:
                con_state[source_name] = False

    def process_signal(source_name: str, name: str, signal: bool):
        nonlocal high_count, low_count
        if signal:
            high_count += 1
        else:
            low_count += 1

        if name not in modules:
            debug("Reciveing on", name, signal)
            return

        module = modules[name]
        out_signal: bool | None = None
        if module[0] == '%':
            if not signal:
                flipflip_states[name] = not flipflip_states[name]
                out_signal = flipflip_states[name]
        else:
            state = conjunction_states[name]
            state[source_name] = signal
            out_signal = len([True for _ in state.values() if not _]) > 0

        if out_signal is not None:
            debug("Sending", out_signal, "from",
                  name, "to", ', '.join(module[1]))
            for dest_name in module[1]:
                queue.append((name, dest_name, out_signal))

    def button():
        nonlocal low_count
        low_count += 1
        debug("Sending", False, "from",
              "broadcast", "to", ', '.join(broadcaster[1]))
        for module in broadcaster[1]:
            queue.append(('broadcaster', module, False))
        while queue:
            process_signal(*queue.pop(0))

    for _ in range(1000):
        button()

    debug("high", high_count, "low", low_count)

    result = low_count * high_count

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
