# https://adventofcode.com/2022/day/19
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

    def sub_inventory(inventory: Inventory, sub: Inventory, count: int) -> Inventory:
        return Inventory(
            ore=inventory.ore - count * sub.ore,
            obsidian=inventory.obsidian - count * sub.obsidian,
            clay=inventory.clay - count * sub.clay,
            geode=inventory.geode - count * sub.geode
        )

    def add_robots(robots: Robots, add: Robots) -> Robots:
        return Robots(
            ore=robots.ore + add.ore,
            obsidian=robots.obsidian + add.obsidian,
            clay=robots.clay + add.clay,
            geode=robots.geode + add.geode
        )

    def factory(inventory: Inventory, blueprint: Blueprint) -> list[tuple[Robots, Cost]]:
        result: list[tuple[Robots, Cost]] = []
        free_choice: bool = False
        for ore_count in range(get_max_robots(inventory, blueprint.ore_robot)+1):
            ore_i = sub_cost(inventory, blueprint.ore_robot, ore_count)
            for obsidian_count in range(get_max_robots(ore_i, blueprint.obsidian_robot)+1):
                obisidan_i = sub_cost(
                    ore_i, blueprint.obsidian_robot, obsidian_count)
                for clay_count in range(get_max_robots(obisidan_i, blueprint.clay_robot)+1):
                    clay_i = sub_cost(
                        obisidan_i, blueprint.clay_robot, clay_count)
                    for geode_count in range(get_max_robots(clay_i, blueprint.geode_robot)+1):
                        if ore_count + obsidian_count + clay_count + geode_count == 0:
                            continue
                        if ore_count * obsidian_count * clay_count * geode_count:
                            free_choice = True
                        result.append((
                            Robots(
                                ore=ore_count,
                                obsidian=obsidian_count,
                                clay=clay_count,
                                geode=geode_count
                            ),
                            Cost(
                                ore=ore_count * blueprint.ore_robot.ore + obsidian_count * blueprint.obsidian_robot.ore +
                                clay_count * blueprint.clay_robot.ore + geode_count * blueprint.geode_robot.ore,
                                obsidian=ore_count * blueprint.ore_robot.obsidian + obsidian_count * blueprint.obsidian_robot.obsidian +
                                clay_count * blueprint.clay_robot.obsidian +
                                geode_count * blueprint.geode_robot.obsidian,
                                clay=ore_count * blueprint.ore_robot.clay + obsidian_count * blueprint.obsidian_robot.clay +
                                clay_count * blueprint.clay_robot.clay +
                                geode_count * blueprint.geode_robot.clay,
                            )
                        ))

        if not free_choice:
            result.append((Robots(0, 0, 0, 0), Cost(0)))
        return result

    _time_stat = [0 for _ in range(MAX_TIME + 2)]

    def minute(time: int, robots: Robots, inventory: Inventory, blueprint: Blueprint) -> int:
        if time > MAX_TIME:
            print(time, inventory.geode, robots, inventory)
            print(_time_stat)
            return inventory.geode

        _time_stat[time] += 1

        # print(time, "a", robots, inventory)

        new_robot_possibilities = factory(inventory, blueprint)
        new_inventory = ore_work(robots.ore, inventory)
        new_inventory = clay_work(robots.clay, new_inventory)
        new_inventory = obisidan_work(robots.obsidian, new_inventory)
        new_inventory = geode_work(robots.geode, new_inventory)

        if time >= 0:
            # print(time, "b", len(new_robot_possibilities), new_inventory)
            if time == 0:
                print(time, robots, inventory)

        if new_robot_possibilities:
            max_geode = 0
            for possibility, cost in new_robot_possibilities:
                max_geode = max(
                    max_geode,
                    minute(
                        time+1,
                        add_robots(possibility, robots), sub_cost(
                            new_inventory, cost
                        ), blueprint
                    )
                )
            return max_geode
        else:
            return minute(time+1, robots, new_inventory, blueprint)

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
        break

    return result


# ---
result = run()
print(result)
open(path/("result" + part + ext), "w").write(str(result).rstrip() + "\n")
