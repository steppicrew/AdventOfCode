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

    connected_devices: dict[str, set[str]] = {}
    all_connections: list[tuple[str, str]] = []

    for input in inputs:
        name, _con_devs = input.split(": ")
        con_devs = _con_devs.split(" ")
        if name not in connected_devices:
            connected_devices[name] = set()
        connected_devices[name] = set((*connected_devices[name], *con_devs))
        for _name in con_devs:
            if _name not in connected_devices:
                connected_devices[_name] = set()
            connected_devices[_name].add(name)
            all_connections.append((name, _name))

    device_connections: dict[str, set[tuple[str, str]]] = {
        d: set()
        for d in connected_devices
    }
    for c in all_connections:
        device_connections[c[0]].add(c)
        device_connections[c[1]].add(c)

    def split_conns(*cons: tuple[str, str]) -> set[str]:
        _devices = {**connected_devices}
        result: set[str] = set()
        for c in cons:
            _devices[c[0]] = set(_ for _ in _devices[c[0]] if _ != c[1])
            _devices[c[1]] = set(_ for _ in _devices[c[1]] if _ != c[0])
        queue = set([n for n in _devices.keys()][:1])
        while queue:
            name = queue.pop()
            result.add(name)
            for name2 in _devices[name]:
                if name2 not in result:
                    queue.add(name2)

        return result

    count = 0

    all_connections.sort(key=lambda c:
                         len(connected_devices[c[0]]) * len(connected_devices[c[1]]))

    """
    devices: list[str] = list(connected_devices.keys())
    devices.sort(key=lambda d: len(connected_devices[d]))

    print(devices[0])
    print(device_connections[devices[0]])
    print(devices[1])
    print(device_connections[devices[1]])
    print(devices[2])
    print(device_connections[devices[2]])
    print(devices[3])
    print(device_connections[devices[3]])
    exit()
    """

    connection_counts: dict[str, dict[str, int]] = {}

    for device, next_devices in connected_devices.items():
        connection_counts[device] = connections = {}

        for d in next_devices:
            visited: set[str] = set((device, d))
            queue: list[str] = [d]
            while queue:
                device = queue.pop(0)
                visited.add(device)
                for _d in connected_devices[device]:
                    if _d in visited:
                        continue
                    queue.append(_d)
            visited.remove(device)

            for _d in visited:
                if _d in next_devices:
                    if _d in connections:
                        connections[_d] += 1
                    else:
                        connections[_d] = 1

    min_count = min(
        count
        for devices in connection_counts.values()
        for count in devices.values()
    )
    print("min", min_count)
    print("count min", len([count for devices in connection_counts.values()
          for count in devices.values() if count == min_count]))

    next_device = "pzl"
    # d = "hfx"
    print(connected_devices[next_device])
    print(connection_counts[next_device])

    exit()

    for i1, c1 in enumerate(all_connections):
        for i2, c2 in enumerate(all_connections[i1+1:]):
            if c1 == c2:
                continue
            for c3 in all_connections[i1+i2+1:]:
                if c1 == c3 or c2 == c3:
                    continue
                count += 1
                if count % 1000 == 0:
                    print(count)
                split = split_conns(c1, c2, c3)
                if 0 < len(split) < len(connected_devices):
                    print(len(split), len(connected_devices))
                    print(len(split) * (len(connected_devices) - len(split)))
                    exit()

    return result


# ---
result: int = run()
print(result)
with open(file=path/("result" + part + EXT), mode="w", encoding='utf-8') as file:
    file.write(str(result).rstrip() + "\n")
