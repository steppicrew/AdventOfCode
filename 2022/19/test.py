from math import ceil


Inventory = Robots = Cost = tuple[int, int, int, int]
ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

NONE = (0, 0, 0, 0)
ONE_ORE = (1, 0, 0, 0)
ONE_CLAY = (0, 1, 0, 0)
ONE_OBSIDIAN = (0, 0, 1, 0)
ONE_GEODE = (0, 0, 0, 1)

blueprint = (
    (4, 0, 0, 0),
    (2, 0, 0, 0),
    (3, 14, 0, 0),
    (2, 0, 7, 0),
)
max_robots = tuple(
    max(b[i] for b in blueprint) for i in range(len(blueprint[0]))
)

print(max_robots)


def add(s1: tuple[int, int, int, int], s2: tuple[int, int, int, int], factor: int = 1):
    return tuple(_s1 + _s2 * factor for _s1, _s2 in zip(s1, s2))


def time_until_ore(ore_needed: int, robots: Robots, inventory: Inventory, time: int) -> tuple[int, Inventory, Robots, list[str]]:
    t_until_next_ore_robot = ceil(
        (blueprint[ORE][ORE] - inventory[ORE]) / robots[ORE]) + 1
    t_remain = max(0, ceil((ore_needed - inventory[ORE]) / robots[ORE]))

    if t_remain > t_until_next_ore_robot \
            and robots[ORE] < ore_needed - inventory[ORE] \
            and robots[ORE] < max_robots[ORE]:
        result = time_until_ore(
            ore_needed=ore_needed,
            robots=add(robots, ONE_ORE),
            inventory=add(
                add(
                    inventory,
                    robots,
                    t_until_next_ore_robot
                ),
                ONE_ORE, -blueprint[ORE][ORE]
            ),
            time=time + t_until_next_ore_robot
        )
        if result[0] <= t_remain:
            return (
                result[0] + t_until_next_ore_robot,
                result[1],
                result[2],
                [f"{time + t_until_next_ore_robot - 1}: ore"] + result[3],
            )

    final_inventory = add(inventory, robots, t_remain)
    return (t_remain, final_inventory, robots, [])


def time_until_next_obsidian(robots: Robots, inventory: Inventory, time: int) -> list[tuple[int, Inventory, Robots, list[str]]]:
    clay_needed = blueprint[OBSIDIAN][CLAY]
    t_until_next_clay_robot = ceil(
        (blueprint[CLAY][ORE] - inventory[ORE]) / robots[ORE]) + 1
    t_until_next_ore_robot = ceil(
        (blueprint[ORE][ORE] - inventory[ORE]) / robots[ORE]) + 1
    t_remain = max(
        0,
        ceil(
            (clay_needed - inventory[CLAY]) / robots[CLAY]
        ) if robots[CLAY] else 1_000
    )

    results: list[tuple[int, Inventory, Robots, list[str]]] = []

    if t_remain > t_until_next_clay_robot:
        result = time_until_next_obsidian(
            robots=add(robots, ONE_CLAY),
            inventory=add(
                add(
                    inventory,
                    robots,
                    t_until_next_clay_robot
                ),
                ONE_ORE, -blueprint[CLAY][ORE]
            ),
            time=time + t_until_next_clay_robot
        )
        results += [(
            r[0] + t_until_next_clay_robot,
            r[1],
            r[2],
            [f"{time + t_until_next_clay_robot - 1}: clay"] + r[3]
        ) for r in result]

    if t_remain > t_until_next_ore_robot and robots[ORE] < max_robots[ORE]:
        result = time_until_next_obsidian(
            robots=add(robots, ONE_ORE),
            inventory=add(
                add(
                    inventory,
                    robots,
                    t_until_next_ore_robot
                ),
                ONE_ORE, -blueprint[ORE][ORE]
            ),
            time=time + t_until_next_ore_robot
        )
        results += [(
            r[0] + t_until_next_ore_robot,
            r[1],
            r[2],
            [f"{time + t_until_next_ore_robot - 1}: ore"] + r[3],
        ) for r in result]

    if results:
        results.sort(key=lambda r: r[0])
        return results

    '''
    print("Clay/Clay final", inventory[CLAY],
            inventory[CLAY] + t_remain * robots[CLAY])
    print("Robots", robots)
    print("Time/Remain", time, t_remain)
    '''

    final_inventory = add(inventory, robots, t_remain)
    if final_inventory[ORE] < blueprint[OBSIDIAN][ORE]:
        result = time_until_ore(
            blueprint[OBSIDIAN][ORE], robots=robots, inventory=final_inventory, time=0)
        print("Remaining ORE", final_inventory, blueprint[OBSIDIAN], result)
        return [(t_remain + result[0], result[1], result[2], [f"Waiting for ORE for {result[0]}"] + result[3])]
    return [(t_remain, final_inventory, robots, [])]


results = time_until_next_obsidian(ONE_ORE, (0, 0, 0, 0), time=0)
for result in results:
    print(result)
