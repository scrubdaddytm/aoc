from aoc.cli import file_input
from dataclasses import dataclass
import re
from math import ceil
from math import prod


@dataclass
class Blueprint:
    ore: int  # ore
    clay: int  # ore
    obsidian: tuple[int, int]  # ore, clay
    geode: tuple[int, int]  # ore, obsidian


def get_max_geodes(blueprint: Blueprint, max_time: int = 24) -> int:
    max_at_robots = {}

    max_ore_bots = max(blueprint.ore, blueprint.clay, blueprint.obsidian[0], blueprint.geode[0])
    max_clay_bots = blueprint.obsidian[1]
    max_obsidian_bots = blueprint.geode[1]

    class Max:
        current_max = 0

    def backtrack(depth, ore_robots, ore, clay_robots, clay, obsidian_robots, obsidian, geo_robots, geodes) -> int:
        robot_key = f"{ore_robots, clay_robots, obsidian_robots, geo_robots}"
        if depth == max_time:
            total_geodes = geodes + geo_robots
            max_at_robots[robot_key] = max(total_geodes, max_at_robots.get(robot_key, 0))
            if total_geodes > Max.current_max:
                Max.current_max = total_geodes
            return total_geodes

        max_geodes = []
        were_growing = False

        if obsidian_robots > 0:
            ore_needed = max(0, blueprint.geode[0] - ore)
            obsidian_needed = max(0, blueprint.geode[1] - obsidian)
            time_to_robot = max(ceil(ore_needed / ore_robots), ceil(obsidian_needed / obsidian_robots)) + 1

            theoretical_max = geodes + (sum([geo_robots + i for i in range(1, max_time - depth + 2)]))
            if Max.current_max > theoretical_max:
                return 0

            if depth + time_to_robot <= max_time:
                max_geodes.append(
                    backtrack(
                        depth + time_to_robot,
                        ore_robots,
                        ore - blueprint.geode[0] + (ore_robots * time_to_robot),
                        clay_robots,
                        clay + (clay_robots * time_to_robot),
                        obsidian_robots,
                        obsidian - blueprint.geode[1] + (obsidian_robots * time_to_robot),
                        geo_robots + 1,
                        geodes + (geo_robots * time_to_robot),
                    )
                )
            were_growing = True
        if clay_robots > 0 and obsidian_robots < max_obsidian_bots:
            ore_needed = max(0, blueprint.obsidian[0] - ore)
            clay_needed = max(0, blueprint.obsidian[1] - clay)
            time_to_robot = max(ceil(ore_needed / ore_robots), ceil(clay_needed / clay_robots)) + 1
            if depth + time_to_robot <= max_time:
                max_geodes.append(
                    backtrack(
                        depth + time_to_robot,
                        ore_robots,
                        ore - blueprint.obsidian[0] + (ore_robots * time_to_robot),
                        clay_robots,
                        clay - blueprint.obsidian[1] + (clay_robots * time_to_robot),
                        obsidian_robots + 1,
                        obsidian + (obsidian_robots * time_to_robot),
                        geo_robots,
                        geodes + (geo_robots * time_to_robot),
                    )
                )
            were_growing = True
        if clay_robots < max_clay_bots:
            ore_needed = max(0, blueprint.clay - ore)
            time_to_robot = ceil(ore_needed / ore_robots) + 1
            if depth + time_to_robot <= max_time:
                max_geodes.append(
                    backtrack(
                        depth + time_to_robot,
                        ore_robots,
                        ore - blueprint.clay + (ore_robots * time_to_robot),
                        clay_robots + 1,
                        clay + (clay_robots * time_to_robot),
                        obsidian_robots,
                        obsidian + (obsidian_robots * time_to_robot),
                        geo_robots,
                        geodes + (geo_robots * time_to_robot),
                    )
                )
            were_growing = True
        if ore_robots < max_ore_bots:
            ore_needed = max(0, blueprint.ore - ore)
            time_to_robot = ceil(ore_needed / ore_robots) + 1
            if depth + time_to_robot <= max_time:
                max_geodes.append(
                    backtrack(
                        depth + time_to_robot,
                        ore_robots + 1,
                        ore - blueprint.ore + (ore_robots * time_to_robot),
                        clay_robots,
                        clay + (clay_robots * time_to_robot),
                        obsidian_robots,
                        obsidian + (obsidian_robots * time_to_robot),
                        geo_robots,
                        geodes + (geo_robots * time_to_robot),
                    )
                )
            were_growing = True

        if not were_growing:
            time_to_robot = 1
            max_geodes.append(
                backtrack(
                    depth + time_to_robot,
                    ore_robots,
                    ore - blueprint.ore + (ore_robots * time_to_robot),
                    clay_robots,
                    clay + (clay_robots * time_to_robot),
                    obsidian_robots,
                    obsidian + (obsidian_robots * time_to_robot),
                    geo_robots,
                    geodes + (geo_robots * time_to_robot),
                )
            )
        total_geodes = max(max_geodes) if max_geodes else 0
        return total_geodes

    max_geodes = backtrack(1, 1, 0, 0, 0, 0, 0, 0, 0)
    # for k, v in max_at_robots.items():
    #     if v == max_geodes:
    #         print(k)
    return max_geodes


def main() -> None:
    blueprints = []
    with file_input() as file:
        p = re.compile(r"Each (ore|clay|obsidian|geode) robot costs (\d+) ore(\.)?( and )?(\d+)?( clay| obsidian)?.?")
        while line := file.readline():
            costs = {}
            for match in re.findall(p, line):
                if match[0] == "ore":
                    costs["ore"] = int(match[1])
                elif match[0] == "clay":
                    costs["clay"] = int(match[1])
                elif match[0] == "obsidian":
                    costs["obsidian"] = (int(match[1]), int(match[4]))
                else:
                    costs["geode"] = (int(match[1]), int(match[4]))
            blueprints.append(Blueprint(**costs))

    for blueprint in blueprints:
        print(f"{blueprint}")

    quality = []
    for idx, blueprint in enumerate(blueprints, 1):
        geodes = get_max_geodes(blueprint)
        quality.append(geodes * idx)
        print(f"{idx}: {geodes} * {idx} = {geodes*idx}")

    print(f"PART 1: {sum(quality)}")

    geodes = []
    for idx, blueprint in enumerate(blueprints[0:3], 1):
        geodes.append(get_max_geodes(blueprint, 32))
        print(f"{idx}: {geodes[-1]}")

    print(f"PART 2: {prod(geodes)}")


if __name__ == "__main__":
    main()
