# https://adventofcode.com/2022/day/19
from math import ceil, floor, sqrt
from pathlib import Path
from functools import reduce
import re
from typing import Callable, NamedTuple, Tuple
import json

ref = 1
part_match = re.search(r'_(\d+)\.py', __file__)
part = "_" + part_match[1] if part_match else ""

ext = "_ref" + str(ref) + ".txt" if ref else ".txt"
path = Path(__file__).parent.absolute()
inputs = open(path/("input" + ext), "r").read().rstrip().split("\n")
# ---


def run():
    result = 0

    MAX_TIME = 24
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3

    NONE = (0, 0, 0, 0)
    ONE_ORE = (1, 0, 0, 0)
    ONE_CLAY = (0, 1, 0, 0)
    ONE_OBSIDIAN = (0, 0, 1, 0)
    ONE_GEODE = (0, 0, 0, 1)

    Inventory = Robots = Cost = tuple[int, int, int, int]

    Blueprint = tuple[Cost, Cost, Cost, Cost]

    def add(s1: tuple[int, int, int, int], s2: tuple[int, int, int, int], factor: int = 1):
        return tuple(_s1 + _s2 * factor for _s1, _s2 in zip(s1, s2))

    def sub(m1: tuple[int, int, int, int], m2: tuple[int, int, int, int], factor: int = 1):
        return add(m1, m2, -factor)

    def do_work(inventory: Inventory, robots: Robots):
        return add(inventory, robots)

    blueprints: list[Blueprint] = []

    for input in inputs:
        match = re.match(
            r'Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.',
            input
        )
        if match:
            blueprints.append((
                (int(match[1]), 0, 0, 0),
                (int(match[2]), 0, 0, 0),
                (int(match[3]), int(match[4]), 0, 0),
                (int(match[5]), 0, int(match[6]), 0)
            ))

    def can_build(inventory: Inventory, cost: Cost):
        for i, c in zip(inventory, cost):
            if c > i:
                return False
        return True

    def print_flow(rounds: list[Robots]):
        inventory = NONE
        robots = ONE_ORE
        time = 1
        for round in rounds:
            for count, cost in zip(round, blueprint):
                inventory = sub(inventory, cost, count)
            inventory = do_work(inventory, robots)
            robots = add(robots, round)

            print(time, round, inventory, robots)
            time += 1

    MIN_TIME = 1

    def need_clay(clay_needed: int, ore_count: int, ore_robots: int, clay_robots: int, ore_cost: int, clay_cost: int) -> tuple[int, set[Robots]]:

        # if we reach our limit next time do nothing
        if clay_robots >= clay_needed:
            return (1, {NONE})

        results: set[tuple[int, Robots]] = set()

        # Variant 1: do nothing and wait until my clay robots have harvested enough clay
        if clay_robots:
            results.add((ceil(clay_needed/clay_robots), NONE))

        # Variant 2: wait for the next clay robot and check from there
        time_until_next_clay_robot = max(
            1,
            ceil((clay_cost - ore_count)/ore_robots)
        )
        result = need_clay(
            clay_needed=clay_needed - time_until_next_clay_robot * clay_robots,
            ore_count=ore_count + time_until_next_clay_robot * ore_robots - clay_cost,
            ore_robots=ore_robots,
            clay_robots=clay_robots + 1,
            ore_cost=ore_cost,
            clay_cost=clay_cost
        )
        results.add((time_until_next_clay_robot + result[0], ONE_CLAY))

        if ore_count < ore_cost + clay_cost:
            # Variant 3: wait for the next ore robot
            time_until_next_ore_robot = max(
                1,
                ceil((ore_cost - ore_count)/ore_robots)
            )
            result = need_clay(
                clay_needed=clay_needed - time_until_next_ore_robot * clay_robots,
                ore_count=ore_count + time_until_next_ore_robot * ore_robots - ore_cost,
                ore_robots=ore_robots + 1,
                clay_robots=clay_robots,
                ore_cost=ore_cost,
                clay_cost=clay_cost
            )
            results.add(
                (time_until_next_ore_robot + result[0], ONE_ORE))

        min_time = min(r[0] for r in results if r[0] > 0)
        return (min_time, set(r[1] for r in results if r[0] == min_time))

    def get_best_robots_to_build(inventory: Inventory, robots: Robots, blueprint: Blueprint, time_left: int) -> set[Robots]:
        def better_than_none(needed_ore) -> set[Robots]:
            result: set[Robots] = {NONE}
            if blueprint[CLAY][ORE] + needed_ore <= robots[ORE]:
                result.add(ONE_CLAY)
            if blueprint[ORE][ORE] + needed_ore <= robots[ORE]:
                result.add(ONE_ORE)
            return result

        if can_build(inventory, blueprint[GEODE]):
            return {ONE_GEODE}

        geode_needs_obsidian = blueprint[GEODE][OBSIDIAN] - \
            inventory[OBSIDIAN]
        geode_needs_ore = blueprint[GEODE][ORE] - inventory[ORE]
        geode_time_until_obsidian = geode_needs_obsidian / \
            robots[OBSIDIAN] if robots[OBSIDIAN] else 1_000
        geode_time_until_ore = geode_needs_ore / robots[ORE]
        if geode_time_until_obsidian <= MIN_TIME and geode_time_until_ore <= MIN_TIME:
            return better_than_none(geode_needs_ore)

        if geode_time_until_obsidian > geode_time_until_ore:
            if can_build(inventory, blueprint[OBSIDIAN]):
                return {ONE_OBSIDIAN}

            obsidian_needs_clay = blueprint[OBSIDIAN][CLAY] - \
                inventory[CLAY]
            obsidian_needs_ore = blueprint[OBSIDIAN][ORE] - \
                inventory[ORE]
            obsidian_time_until_clay = obsidian_needs_clay / \
                robots[CLAY] if robots[CLAY] else 1_000
            obsidian_time_until_ore = obsidian_needs_ore / robots[ORE]
            if obsidian_time_until_clay <= MIN_TIME and obsidian_time_until_ore <= MIN_TIME:
                return better_than_none(obsidian_needs_ore)

            if obsidian_time_until_clay > obsidian_time_until_ore:
                best_option = need_clay(
                    clay_needed=obsidian_needs_clay,
                    ore_count=inventory[ORE],
                    ore_robots=robots[ORE],
                    clay_robots=robots[CLAY],
                    ore_cost=blueprint[ORE][ORE],
                    clay_cost=blueprint[CLAY][ORE]
                )
                result: set[Robots] = best_option[1]
                if ONE_ORE in result and not can_build(inventory, blueprint[ORE]):
                    result.remove(ONE_ORE)
                if ONE_CLAY in result and not can_build(inventory, blueprint[CLAY]):
                    result.remove(ONE_CLAY)
                return result if result else {NONE}

            elif can_build(inventory, blueprint[ORE]):
                return {ONE_ORE}

        elif can_build(inventory, blueprint[ORE]):
            return {ONE_ORE}

        return {NONE}

    next_thread_id = 1

    def minute(time: int, thread: int, prefix: str, robots: Robots, inventory: Inventory, blueprint: Blueprint) -> tuple[int, list[Robots]]:
        if time == MAX_TIME:
            # print(time, inventory.geode, robots, inventory)
            return (inventory[GEODE], [])

        new_robots = get_best_robots_to_build(
            inventory, robots, blueprint, MAX_TIME - time)

        old_inventory = inventory

        results: list[tuple[int, list[Robots]]] = []

        _thread = thread

        thread_prefix = prefix
        if len(new_robots) > 1:
            print()
            print(f"{prefix}**** Starting new threads", time + 1, new_robots)
            thread_prefix += "  "

        for i, new_robot in enumerate(new_robots):
            if len(new_robots) > 1:
                nonlocal next_thread_id
                _thread = next_thread_id
                next_thread_id += 1

            inventory = old_inventory

            for count, cost in zip(new_robot, blueprint):
                inventory = sub(inventory, cost, count)

            inventory = do_work(robots, inventory)

            if new_robot[ORE]:
                print(f"{thread_prefix}Minute", time + 1, _thread, "Buy ore-robot      for",
                      blueprint[ORE], f"have {old_inventory}->{inventory}")
            elif new_robot[CLAY]:
                print(f"{thread_prefix}Minute", time + 1, _thread, "Buy clay-robot     for",
                      blueprint[CLAY], f"have {old_inventory}->{inventory}")
            elif new_robot[OBSIDIAN]:
                print(f"{thread_prefix}Minute", time + 1, _thread, "Buy obsidian-robot for",
                      blueprint[OBSIDIAN], f"have {old_inventory}->{inventory}")
            elif new_robot[GEODE]:
                print(f"{thread_prefix}Minute", time + 1, _thread, "Buy geode-robot    for",
                      blueprint[GEODE], f"have {old_inventory}->{inventory}")

            result = minute(time+1, _thread, thread_prefix, add(robots, new_robot),
                            inventory, blueprint)

            results.append((result[0], [new_robot] + result[1]))

            if len(new_robots) > i + 1:
                print(f"{prefix}****")

        if len(new_robots) > 1:
            print(f"{prefix}**** Returned thread", time +
                  1, _thread, thread, results)
            print()

        return max(results, key=lambda r: r[0])

    results: list[int] = []
    for blueprint in blueprints[1:]:
        r1 = minute(
            0, 0, "",
            ONE_ORE,
            NONE,
            blueprint
        )
        # print_flow(r1[1])

        results.append(r1[0])
        break

    max_result = max(results)
    for i, r in enumerate(results):
        if r == max_result:
            result = (i+1) * r
            break

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
