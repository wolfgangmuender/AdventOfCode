import os
import time
from copy import deepcopy

from more_itertools import set_partitions


def solve(puzzle_input):
    valves = {}
    for line in puzzle_input:
        valve, tunnels = line.split("; ")
        tunnel_offset = 23 if "tunnels" in tunnels else 22
        valve_id, flow_rate_str = valve[6:].split(" has flow rate=")
        flow_rate = int(flow_rate_str)

        valves[valve_id] = {
            "flow_rate": flow_rate,
            "tunnels": tunnels[tunnel_offset:].split(", "),
        }

    relevant_valves = {}
    for valve_id, valve in valves.items():
        if valve_id == "AA" or valve["flow_rate"] > 0:
            relevant_valves[valve_id] = {
                "flow_rate": valve["flow_rate"],
                "tunnels": get_connections_to_relevant_valves(valve_id, valves),
            }

    total_flow_rate = sum([valve["flow_rate"] for valve in valves.values()])

    start_path = {
        "minutes": 0,
        "curr_valve": "AA",
        "flow_rate": 0,
        "open_valves": [],
        "released": 0,
    }

    print("Solution 1: {}".format(get_max_released(relevant_valves, total_flow_rate, start_path, 30, {}, 0)))

    openable_valves = list(relevant_valves.keys())
    openable_valves.remove("AA")

    all_released = []
    cache = []
    for my_valve_ids, elephant_valve_ids in set_partitions(openable_valves, 2):
        if my_valve_ids in cache:
            continue
        else:
            cache.append(elephant_valve_ids)

        my_valves = filter_valves(relevant_valves, my_valve_ids)
        my_total_flow_rate = sum([valve["flow_rate"] for valve in my_valves.values()])
        my_released = get_max_released(my_valves, my_total_flow_rate, start_path, 26, {}, 0)

        elephant_valves = filter_valves(relevant_valves, elephant_valve_ids)
        elephant_total_flow_rate = sum([valve["flow_rate"] for valve in elephant_valves.values()])
        elephant_released = get_max_released(elephant_valves, elephant_total_flow_rate, start_path, 26, {}, 0)

        all_released.append(my_released + elephant_released)

    print("Solution 2: {}".format(max(all_released)))


def get_connections_to_relevant_valves(valve_id, valves):
    tunnels_to_relevant_valves = {}

    visited = [valve_id]
    queue = [[next_valve_id] for next_valve_id in valves[valve_id]["tunnels"]]
    while queue:
        curr_path = queue.pop(0)
        curr_valve_id = curr_path[-1]

        visited.append(curr_valve_id)

        if valves[curr_valve_id]["flow_rate"] > 0:
            tunnels_to_relevant_valves[curr_valve_id] = len(curr_path)
        for next_valve_id in valves[curr_valve_id]["tunnels"]:
            if next_valve_id not in visited:
                queue.append([v for v in curr_path] + [next_valve_id])

    return tunnels_to_relevant_valves


def get_max_released(valves, total_flow_rate, curr_path, max_minutes, cache, current_best):
    if curr_path["minutes"] == max_minutes:
        return curr_path["released"]

    if current_best - curr_path["released"] > total_flow_rate * (max_minutes - curr_path["minutes"]):
        return -1

    new_paths = _go_on(valves, max_minutes, curr_path)

    if curr_path["flow_rate"] == total_flow_rate or not new_paths:
        remaining_minutes = max_minutes - curr_path["minutes"]
        return curr_path["released"] + curr_path["flow_rate"] * remaining_minutes

    all_released = []
    for new_path in new_paths:
        if get_key(new_path) in cache:
            all_released.append(cache[get_key(new_path)])
        else:
            released = get_max_released(valves, total_flow_rate, new_path, max_minutes, cache, max(all_released + [current_best]))
            cache[get_key(new_path)] = released
            all_released.append(released)

    return max(all_released)


def _go_on(valves, max_minutes, curr_path):
    new_candidates = []

    curr_id = curr_path["curr_valve"]
    if curr_id == "AA" or curr_id in curr_path["open_valves"]:
        tunnels = valves[curr_id]["tunnels"]
        for valve_id, minutes in tunnels.items():
            if valve_id in curr_path["open_valves"]:
                continue
            if curr_path["minutes"] + minutes > max_minutes:
                continue
            new_path = deepcopy(curr_path)
            new_path["minutes"] += minutes
            new_path["curr_valve"] = valve_id
            new_path["released"] += new_path["flow_rate"] * minutes
            new_candidates.append(new_path)
    else:
        new_path = deepcopy(curr_path)
        new_path["minutes"] += 1
        new_path["curr_valve"] = curr_id
        new_path["released"] += new_path["flow_rate"]
        new_path["open_valves"].append(curr_id)
        new_path["flow_rate"] += valves[curr_id]["flow_rate"]
        new_candidates.append(new_path)

    return new_candidates


def get_key(curr_path):
    cache_key = f"{curr_path['minutes']}_{curr_path['curr_valve']}"
    cache_key += "_" + "-".join([open_valve for open_valve in sorted(curr_path['open_valves'])])
    cache_key += f"_{curr_path['released']}"
    return cache_key


def filter_valves(valves, allowed_valves):
    filtered_valves = {}

    all_allowed_valves = [v for v in allowed_valves] + ["AA"]
    for valve_id, valve in valves.items():
        if valve_id in all_allowed_valves:
            filtered_valves[valve_id] = {
                "flow_rate": valve["flow_rate"],
                "tunnels": {tunnel_id: tunnel for tunnel_id, tunnel in valve["tunnels"].items() if tunnel_id in all_allowed_valves},
            }

    return filtered_valves


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
