import os
import time
from copy import deepcopy


def solve(puzzle_input):
    blueprints = []
    for line in puzzle_input:
        parts = line.split(" Each ")
        blueprints.append({
            "id": int(parts[0][10:-1]),
            "ore": _get_cost(parts[1]),
            "clay": _get_cost(parts[2]),
            "obsidian": _get_cost(parts[3]),
            "geode": _get_cost(parts[4]),
        })

    print("Solution 1: {}".format(sum([_find_max_geodes(blueprint, 24) * blueprint["id"] for blueprint in blueprints])))  # 10105s
    geodes1 = _find_max_geodes(blueprints[0], 32)
    geodes2 = _find_max_geodes(blueprints[1], 32)
    geodes3 = _find_max_geodes(blueprints[2], 32)
    print("Solution 2: {}".format(geodes1 * geodes2 * geodes3))  # takes ~1.5 days


def _find_max_geodes(blueprint, max_minutes):
    strategy = {
        "robots": {
            "ore": 1,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        },
        "resources": {
            "ore": 0,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        },
        "minutes": 0
    }
    cache = {}

    max_geodes = _apply_strategy(blueprint, max_minutes, strategy, cache)
    print(max_geodes)

    return max_geodes


def _apply_strategy(blueprint, max_minutes, strategy, cache):
    if len(cache) % 1000000 == 0:
        print(len(cache))

    cache_key = _cache_key(strategy)
    if cache_key in cache:
        return cache[cache_key]

    if strategy["minutes"] == max_minutes:
        return strategy["resources"]["geode"]

    geode_count = []

    if _can_afford(blueprint["geode"], strategy):
        new_strategy = deepcopy(strategy)
        _collect(new_strategy)
        _construct(blueprint, "geode", new_strategy)
        geode_count.append(_apply_strategy(blueprint, max_minutes, new_strategy, cache))
    else:
        new_strategy = deepcopy(strategy)
        _collect(new_strategy)
        geode_count.append(_apply_strategy(blueprint, max_minutes, new_strategy, cache))

        if _can_afford(blueprint["obsidian"], strategy):
            new_strategy = deepcopy(strategy)
            _collect(new_strategy)
            _construct(blueprint, "obsidian", new_strategy)
            geode_count.append(_apply_strategy(blueprint, max_minutes, new_strategy, cache))

        if _can_afford(blueprint["clay"], strategy):
            new_strategy = deepcopy(strategy)
            _collect(new_strategy)
            _construct(blueprint, "clay", new_strategy)
            geode_count.append(_apply_strategy(blueprint, max_minutes, new_strategy, cache))

        if _can_afford(blueprint["ore"], strategy):
            new_strategy = deepcopy(strategy)
            _collect(new_strategy)
            _construct(blueprint, "ore", new_strategy)
            geode_count.append(_apply_strategy(blueprint, max_minutes, new_strategy, cache))

    max_geode_count = max(geode_count)

    cache[_cache_key(strategy)] = max_geode_count

    return max_geode_count


def _cache_key(strategy):
    return hash(str(strategy))


def _extrapolate(strategy):
    diff = 24 - strategy["minutes"]
    return strategy["resources"]["geode"] + diff*strategy["robots"]["geode"] + sum(range(0, diff))


def _collect(strategy):
    strategy["minutes"] += 1
    for unit, num in strategy["robots"].items():
        strategy["resources"][unit] += num


def _can_afford(robot, resources):
    for unit, num in robot.items():
        if resources["resources"][unit] < num:
            return False
    return True


def _construct(blueprint, robot, strategy):
    for unit, num in blueprint[robot].items():
        strategy["resources"][unit] -= num
    strategy["robots"][robot] += 1


def _get_cost(cost_str):
    costs = {}

    _, costs_part = cost_str[:-1].split("costs ")
    costs_str = costs_part.split(" and ")
    for cost in costs_str:
        num, unit = cost.split(" ")
        costs[unit] = int(num)

    return costs


def main():
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    solve(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))


if __name__ == "__main__":
    main()
