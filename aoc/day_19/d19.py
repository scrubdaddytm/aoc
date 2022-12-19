from aoc.cli import file_input
from dataclasses import dataclass
import re


GCR = "GEODE_CRACKING_ROBOT"
OCR = "OBSIDIAN_COLLECTING_ROBOT"
CCR = "CLAY_COLLECTING_ROBOT"
ORE = "ORE_COLLECTING_ROBOT"

@dataclass
class Blueprint:
    ore: int #ore
    clay: int #ore
    obsidian: tuple[int, int] #ore, clay
    geode: tuple[int, int] #ore, obsidian


def get_max_geodes(bp: Blueprint) -> int:
    # this aint it
    cache = {}
    best_at_depth = [0 for _ in range(24)]
    def backtrack(depth, ore_coll, ore, ccr, clay, ocr, obsidian, gcr, geo) -> int:
        cache_key = f"{ocr},{ore},{ccr},{clay},{ocr},{obsidian},{gcr}"
        if cache.get(cache_key):
            return cache[cache_key]
        if depth == 24:
            cache[cache_key] = geo+gcr
            return geo + gcr

        max_geodes = [0, 0, 0, 0, 0]
        # print(f"Exploring {depth} with {cache_key}")
        if ore >= bp.geode[0] and obsidian >= bp.geode[1]:
            max_geodes[0] = backtrack(depth+1, ore_coll, ore-bp.geode[0]+ore_coll, ccr, clay+ccr, ocr, obsidian-bp.geode[1]+ocr, gcr+1, geo+gcr)
        if ore >= bp.obsidian[0] and clay >= bp.obsidian[1]:
            max_geodes[1] = backtrack(depth+1, ore_coll, ore-bp.obsidian[0]+ore_coll, ccr, clay-bp.obsidian[1]+ccr, ocr+1, obsidian+ocr, gcr, geo+gcr)
        if ore >= bp.clay:
            max_geodes[2] = backtrack(depth+1, ore_coll, ore-bp.clay+ore_coll, ccr+1, clay+ccr, ocr, obsidian+ocr, gcr, geo+gcr)
        if ore >= bp.ore:
            max_geodes[3] = backtrack(depth+1, ore_coll+1, ore-bp.ore+ore_coll, ccr, clay+ccr, ocr, obsidian+ocr, gcr, geo+gcr)
        max_geodes[4] = backtrack(depth+1, ore_coll, ore+ore_coll, ccr, clay+ccr, ocr, obsidian+ocr, gcr, geo+gcr)

        max_idx = 0
        for idx in range(1, 5):
            max_idx = max_idx if max_geodes[idx] < max_geodes[max_idx] else idx
        best_at_depth[depth-1] = max(best_at_depth[depth-1], max_geodes[max_idx])

        return max(max_geodes)

    return backtrack(1, 1, 0, 0, 0, 0, 0, 0, 0)


def main() -> None:
    blueprints = []
    with file_input() as file:
        p = re.compile(r"  Each (ore|clay|obsidian|geode) robot costs (\d+) ore(\.)?( and )?(\d+)?( clay| obsidian)?.?")
        while line := file.readline():
            if line.startswith("Blueprint"):
                costs = {}
                for _ in range(4):
                    line = file.readline()
                    bp = p.match(line)
                    if bp.group(1) == "ore":
                        costs["ore"] = int(bp.group(2))
                    elif bp.group(1) == "clay":
                        costs["clay"] = int(bp.group(2))
                    elif bp.group(1) == "obsidian":
                        costs["obsidian"] = (int(bp.group(2)), int(bp.group(5)))
                    else:
                        costs["geode"] = (int(bp.group(2)), int(bp.group(5)))
                blueprints.append(Blueprint(**costs))
                file.readline()

    print(f"{blueprints}")

    quality = []
    for idx, blueprint in enumerate(blueprints, 1):
        geodes = get_max_geodes(blueprint)
        quality.append(geodes * idx)
        print(f"{idx}: {geodes} * {idx} = {geodes*idx}")

    print(f"{sum(quality)}")



if __name__ == "__main__":
    main()