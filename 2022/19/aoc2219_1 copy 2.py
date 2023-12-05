# https://adventofcode.com/2022/day/19
from math import floor
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

    class Cost(NamedTuple):
        ore: int
        clay: int = 0
        obsidian: int = 0

    class Blueprint(NamedTuple):
        ore_robot: Cost
        clay_robot: Cost
        obsidian_robot: Cost
        geode_robot: Cost

    class Robots(NamedTuple):
        ore: int
        clay: int
        obsidian: int
        geode: int

    class Inventory(NamedTuple):
        ore: int
        clay: int
        obsidian: int
        geode: int

    def ore_work(count: int, inventory: Inventory) -> Inventory:
        return Inventory(ore=inventory.ore + count, clay=inventory.clay, obsidian=inventory.obsidian, geode=inventory.geode)

    def clay_work(count: int, inventory: Inventory) -> Inventory:
        return Inventory(ore=inventory.ore, clay=inventory.clay + count, obsidian=inventory.obsidian, geode=inventory.geode)

    def obisidan_work(count: int, inventory: Inventory) -> Inventory:
        return Inventory(ore=inventory.ore, clay=inventory.clay, obsidian=inventory.obsidian + count, geode=inventory.geode)

    def geode_work(count: int, inventory: Inventory) -> Inventory:
        return Inventory(ore=inventory.ore, clay=inventory.clay, obsidian=inventory.obsidian, geode=inventory.geode + count)

    blueprints: list[Blueprint] = []

    for input in inputs:
        match = re.match(
            r'Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.',
            input
        )
        if match:
            blueprints.append(Blueprint(
                ore_robot=Cost(ore=int(match[1])),
                clay_robot=Cost(ore=int(match[2])),
                obsidian_robot=Cost(ore=int(match[3]), clay=int(match[4])),
                geode_robot=Cost(ore=int(match[5]), obsidian=int(match[6])),
            ))

    def get_max_robots(inventory: Inventory, cost: Cost) -> int:
        min_count = inventory.ore // cost.ore
        if cost.clay:
            min_count = min(min_count, inventory.clay // cost.clay)
        if cost.obsidian:
            min_count = min(min_count, inventory.obsidian // cost.obsidian)
        return min_count

    def sub_cost(inventory: Inventory, cost: Cost, count: int = 1) -> Inventory:
        return Inventory(
            ore=inventory.ore - count * cost.ore,
            obsidian=inventory.obsidian - count * cost.obsidian,
            clay=inventory.clay - count * cost.clay,
            geode=inventory.geode
        )

    def add_robots(robots: Robots, add: Robots) -> Robots:
        return Robots(
            ore=robots.ore + add.ore,
            obsidian=robots.obsidian + add.obsidian,
            clay=robots.clay + add.clay,
            geode=robots.geode + add.geode
        )

    def get_last_3(count: int):
        return filter(lambda c: c >= 0, (count, count-1, count-2))

    def factory(inventory: Inventory, blueprint: Blueprint) -> set[Robots]:
        result: set[Robots] = set()

        max_geode_count = get_max_robots(inventory, blueprint.geode_robot)
        for geode_count in get_last_3(max_geode_count):
            geode_inventory = sub_cost(
                inventory, blueprint.geode_robot, geode_count)

            max_obsidian_count = get_max_robots(
                geode_inventory, blueprint.obsidian_robot)
            for obsidian_count in get_last_3(max_obsidian_count):
                obsidian_inventory = sub_cost(
                    geode_inventory, blueprint.obsidian_robot, obsidian_count)

                max_clay_count = get_max_robots(
                    obsidian_inventory, blueprint.clay_robot)
                for clay_count in get_last_3(max_clay_count):
                    clay_inventory = sub_cost(
                        obsidian_inventory, blueprint.clay_robot, clay_count)

                    max_ore_count = get_max_robots(
                        clay_inventory, blueprint.ore_robot)
                    for ore_count in get_last_3(max_ore_count):
                        result.add(Robots(
                            ore=ore_count,
                            clay=clay_count,
                            obsidian=obsidian_count,
                            geode=geode_count
                        ))

        return result

    def minute(time: int, robots: Robots, inventory: Inventory, blueprint: Blueprint) -> int:
        if time == MAX_TIME:
            print(time, inventory.geode, robots, inventory)
            return inventory.geode

        # print(time, "a", robots, inventory)

        new_robot_possibilities = factory(inventory, blueprint)

        inventory = ore_work(robots.ore, inventory)
        inventory = clay_work(robots.clay, inventory)
        inventory = obisidan_work(robots.obsidian, inventory)
        inventory = geode_work(robots.geode, inventory)

        max_geode = 0

        for new_robots in new_robot_possibilities:
            new_inventory = Inventory(
                ore=inventory.ore - (
                    new_robots.ore * blueprint.ore_robot.ore
                    + new_robots.clay * blueprint.clay_robot.ore
                    + new_robots.obsidian * blueprint.obsidian_robot.ore
                    + new_robots.geode * blueprint.geode_robot.ore
                ),
                clay=inventory.clay - new_robots.obsidian * blueprint.obsidian_robot.clay,
                obsidian=inventory.obsidian - new_robots.geode * blueprint.geode_robot.obsidian,
                geode=inventory.geode
            )

            max_geode = max(max_geode, minute(
                time+1, add_robots(robots, new_robots), new_inventory, blueprint))

        return max_geode

    for blueprint in blueprints:
        result = max(
            result,
            minute(
                0,
                Robots(ore=1, clay=0, obsidian=0, geode=0),
                Inventory(ore=0, clay=0, obsidian=0, geode=0),
                blueprint
            )
        )

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
