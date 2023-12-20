# https://adventofcode.com/2023/day/01
import re
from math import lcm
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


debug = print_off


def run() -> int:
    result: int = 0

    Module = tuple[str, tuple[str, ...]]
    QueueElement = tuple[str, bool]

    FrozenConjunctionStates = tuple[
        tuple[
            str,
            tuple[tuple[str, bool], ...]
        ], ...
    ]
    FrozenFlipFlopStates = tuple[tuple[str, bool], ...]

    modules: dict[str, Module] = {}
    module_sources: dict[str, list[str]] = {
        'broadcaster': []
    }

    module_queues: dict[str, list[QueueElement]] = {}

    conjunction_states: dict[str, dict[str, bool]] = {}
    flipflop_states: dict[str, bool] = {}

    def freeze_conjunction_states(sources: set[str]) -> FrozenConjunctionStates:
        return tuple(sorted(
            (
                (name, tuple(sorted(
                    (
                        (_name, state)
                        for _name, state in states.items()
                    ),
                    key=lambda s: s[0]
                )))
                for name, states in conjunction_states.items()
                if name in sources
            ),
            key=lambda s: s[0]
        ))

    def freeze_flipflop_states(sources: set[str]) -> FrozenFlipFlopStates:
        return tuple(sorted(
            (
                (name, state)
                for name, state in flipflop_states.items()
                if name in sources
            ),
            key=lambda s: s[0]
        ))

    def freeze_state(sources: set[str]) -> tuple[FrozenConjunctionStates, FrozenFlipFlopStates]:
        return (freeze_conjunction_states(sources), freeze_flipflop_states(sources))

    for input in inputs:
        name, destinations = input.split(' -> ')
        if name == 'broadcaster':
            modules[name] = ('', tuple(destinations.split(', ')))
        else:
            modules[name[1:]] = (name[0], tuple(destinations.split(', ')))

    for name, module in modules.items():
        for dest_name in module[1]:
            if dest_name in module_sources:
                module_sources[dest_name].append(name)
            else:
                module_sources[dest_name] = [name]

    def reset_states():
        module_queues.clear()
        conjunction_states.clear()
        flipflop_states.clear()
        for name, module in modules.items():
            module_queues[name] = []
            if module[0] == '&':
                conjunction_states[name] = {
                    n: False for n in module_sources[name]}
            else:
                flipflop_states[name] = False

    def get_sources(name: str, sources: set[str] | None = None):
        if sources is None:
            sources = set()
        for s in module_sources[name]:
            if s not in sources:
                sources.add(s)
                get_sources(s, sources)
        return sources

    def print_signal(source: str, destinations: tuple[str, ...], signal: bool) -> None:
        for dest in destinations:
            debug(source, '-' + ("high" if signal else "low") + '->', dest)

    def process_signal(name: str, source_name: str, signal: bool):
        module = modules[name]
        out_signal: bool | None = None
        if module[0] == '%':
            if not signal:
                flipflop_states[name] = not flipflop_states[name]
                out_signal = flipflop_states[name]
        elif module[0] == '&':
            state = conjunction_states[name]
            state[source_name] = signal
            out_signal = len([True for _ in state.values() if not _]) > 0
        else:
            out_signal = False

        if out_signal is not None:
            print_signal(name, module[1], out_signal)
            for dest_name in module[1]:
                if dest_name not in module_queues:
                    # debug("Reciveing on", dest_name, signal)
                    pass
                else:
                    module_queues[dest_name].append((name, out_signal))

    def button_press():
        print_signal('button', ("broadcaster",), False)
        module_queues["broadcaster"].append(("button", False))

        while True:
            queues: tuple[tuple[str, QueueElement], ...] = tuple(
                (name, queue.pop(0))
                for name, queue in module_queues.items()
                if queue
            )
            if not queues:
                break

            for queue in queues:
                process_signal(queue[0], *queue[1])

    def get_cycle_count(name: str) -> int:
        sources = get_sources(name)
        reset_states()
        states: set[tuple[FrozenConjunctionStates,
                          FrozenFlipFlopStates]] = set()
        states.add(freeze_state(sources))
        count = 0
        while True:
            count += 1
            button_press()
            new_state = freeze_state(sources)
            if new_state in states:
                return count
            states.add(new_state)

    counts: dict[str, int] = {}
    for name in module_sources[module_sources["rx"][0]] if "rx" in module_sources else modules.keys():
        counts[name] = get_cycle_count(name)

    debug(counts)

    result = lcm(*counts.values())

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
