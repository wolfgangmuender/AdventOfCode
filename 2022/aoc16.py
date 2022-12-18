import os
import time
from copy import deepcopy


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
    total_flow_rate = sum([valve["flow_rate"] for valve in valves.values()])

    print("Solution 1: {}".format(_find_best_path_alone(valves, total_flow_rate, False)["released"]))
    print("Solution 2: {}".format(_find_best_path_alone(valves, total_flow_rate, True)["released"]))
    # Test data
    # 1651 - < 1s
    # 1707 - 24s


def _find_best_path_alone(valves, total_flow_rate, with_elephant):
    max_rounds = 27 if with_elephant else 31
    best_path = None

    candidates = [{
        "valves": ["AA"],
        "elephant_valves": ["AA"],
        "flow_rates": [0],
        "open_valves": [],
        "released": 0,
    }]
    rounds = 0
    start = time.time()
    while candidates:
        rounds += 1
        if rounds % 100000 == 0:
            print(f"{rounds} rounds, {len(candidates)} candidates, {time.time() - start}s")

        curr_path = max(candidates, key=lambda p: p["released"])
        candidates.remove(curr_path)
        if best_path and (best_path["released"] - curr_path["released"]) > total_flow_rate * (max_rounds - len(curr_path["valves"])):
            continue

        if len(curr_path["valves"]) == max_rounds:
            if not best_path or best_path["released"] < curr_path["released"]:
                best_path = curr_path
                print(best_path)
            continue

        new_candidates = _go_on(valves, curr_path)
        if with_elephant:
            new_candidates = _go_on_elephant(valves, new_candidates)

        candidates.extend(new_candidates)

    return best_path


def _go_on(valves, curr_path):
    new_candidates = []

    curr_id = curr_path["valves"][-1]
    tunnels = valves[curr_id]["tunnels"]
    for valve_id in tunnels:
        if len(tunnels) > 1 and len(curr_path["valves"]) > 1 and curr_path["valves"][-2] == valve_id:
            continue
        new_path = deepcopy(curr_path)
        new_path["valves"].append(valve_id)
        new_path["flow_rates"].append(new_path["flow_rates"][-1])
        new_path["released"] += new_path["flow_rates"][-2]
        new_candidates.append(new_path)
    if valves[curr_id]["flow_rate"] > 0 and curr_id not in curr_path["open_valves"]:
        new_path = deepcopy(curr_path)
        new_path["valves"].append(curr_id)
        new_path["flow_rates"].append(new_path["flow_rates"][-1] + valves[curr_id]["flow_rate"])
        new_path["open_valves"].append(curr_id)
        new_path["released"] += new_path["flow_rates"][-2]
        new_candidates.append(new_path)

    return new_candidates


def _go_on_elephant(valves, candidates):
    new_candidates = []

    for candidate in candidates:
        curr_id = candidate["elephant_valves"][-1]
        tunnels = valves[curr_id]["tunnels"]
        for valve_id in tunnels:
            if len(tunnels) > 1 and len(candidate["elephant_valves"]) > 1 and candidate["elephant_valves"][-2] == valve_id:
                continue
            new_path = deepcopy(candidate)
            new_path["elephant_valves"].append(valve_id)
            new_candidates.append(new_path)
        if valves[curr_id]["flow_rate"] > 0 and curr_id not in candidate["open_valves"]:
            new_path = deepcopy(candidate)
            new_path["elephant_valves"].append(curr_id)
            new_path["flow_rates"][-1] += valves[curr_id]["flow_rate"]
            new_path["open_valves"].append(curr_id)
            new_candidates.append(new_path)

    return new_candidates


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
