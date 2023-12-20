import os
import time
from collections import defaultdict, Counter
from copy import copy
from math import lcm

TEST_SOLUTION1 = 11687500
TEST_SOLUTION2 = 3


def solve(puzzle_input):
    modules = {}
    for line in puzzle_input:
        name, destinations = line.split(" -> ")
        if name == "broadcaster":
            module_type = "="
        else:
            module_type = name[0]
            name = name[1:]
        modules[name] = {
            "name": name,
            "type": module_type,
            "destinations": destinations.split(", ")
        }

    signals, _ = get_signals(modules, 1000)

    all_paths = get_all_paths(modules)
    frequencies = []
    for start_module in modules["broadcaster"]["destinations"]:
        frequency = get_steps_until_rx(modules, all_paths, start_module) + 1
        frequencies.append(frequency)

    return signals["low"] * signals["high"], lcm(*frequencies)


def get_steps_until_rx(modules, all_paths, start_module_name):
    filtered_module_names = set()
    for path in all_paths:
        if start_module_name in path:
            filtered_module_names.update(path)

    filtered_modules = {}
    for module in modules.values():
        if module["name"] in filtered_module_names:
            filtered_modules[module["name"]] = {
                "name": module["name"],
                "type": module["type"],
                "destinations": [d for d in module["destinations"] if d in filtered_module_names]
            }

    _, first_low_at = get_signals(filtered_modules, 10000)

    return first_low_at


def get_signals(modules, num_rounds):
    signals = {"low": 0, "high": 0}
    status = init_modules(modules)
    first_low_at = None
    for i in range(0, num_rounds):
        signals["low"] += 1
        ongoing = [["button", "broadcaster", "low"]]
        while ongoing:
            curr = ongoing.pop(0)
            if curr[1] == "rx":
                if curr[2] == "low" and not first_low_at:
                    first_low_at = i
                continue

            sender_name = curr[0]
            receiver = modules[curr[1]]
            pulse = curr[2]
            if receiver["type"] == "%":
                if pulse == "low":
                    status[receiver["name"]] = not status[receiver["name"]]
                    if status[receiver["name"]]:
                        send(receiver, "high", signals, ongoing)
                    else:
                        send(receiver, "low", signals, ongoing)
            elif receiver["type"] == "&":
                status[receiver["name"]][sender_name] = pulse
                counter = Counter(status[receiver["name"]].values())
                new_pulse = "low" if "low" not in counter else "high"
                send(receiver, new_pulse, signals, ongoing)
            elif receiver["type"] == "=":
                send(receiver, pulse, signals, ongoing)
    return signals, first_low_at


def init_modules(modules):
    status = {}
    senders = get_senders(modules)
    for name, module in modules.items():
        if module["type"] == "%":
            status[name] = False
        elif module["type"] == "&":
            status[name] = {sender: "low" for sender in senders[name]}
    return status


def get_senders(modules):
    senders = defaultdict(lambda: set())
    for name, module in modules.items():
        for target in module["destinations"]:
            senders[target].add(name)
    return senders


def send(module, pulse, signals, ongoing):
    for destination in module["destinations"]:
        signals[pulse] += 1
        ongoing.append([module["name"], destination, pulse])


def get_all_paths(modules):
    open_paths = [["broadcaster"]]
    all_paths = []
    while open_paths:
        open_path = open_paths.pop()
        destinations = modules[open_path[-1]]["destinations"]
        for destination in destinations:
            new_path = copy(open_path)
            new_path.append(destination)
            if destination in open_path or destination == "rx":
                all_paths.append(new_path)
            else:
                open_paths.append(new_path)
    return all_paths


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    test_input_file2 = test_input_file.replace(".txt", "-2.txt")
    if os.path.isfile(test_input_file):
        start = time.time()
        with open(test_input_file) as f:
            content1 = f.read().splitlines()
        if os.path.isfile(test_input_file2):
            with open(test_input_file2) as f:
                content2 = f.read().splitlines()
            solution1, _ = solve(content1)
            _, solution2 = solve(content2)
        else:
            solution1, solution2 = solve(content1)
        if solution1 != TEST_SOLUTION1:
            print(f"TEST solution 1 '{solution1}' not correct!")
            return
        if solution2 != TEST_SOLUTION2:
            print(f"TEST solution 2 '{solution2}' not correct!")
            return
        end = time.time()
        print_diff(end - start, True)
    else:
        open(test_input_file, 'a').close()

    input_file = "input/" + os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    if os.path.isfile(input_file):
        with open(input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
        print("Solution 1: {}".format(solution1))
        print("Solution 2: {}".format(solution2))
        end = time.time()
        print_diff(end - start, False)
    else:
        open(input_file, 'a').close()


def print_diff(diff, is_test):
    prefix = "TEST " if is_test else ""
    if diff >= 1:
        print("The {}solutions took {}s".format(prefix, round(diff)))
    else:
        print("The {}solutions took {}ms".format(prefix, round(diff * 1000)))


if __name__ == "__main__":
    main()
