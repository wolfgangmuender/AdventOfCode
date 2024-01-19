import copy
import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 54
TEST_SOLUTION2 = 0


def solve(puzzle_input):
    components = defaultdict(lambda: set())
    for line in puzzle_input:
        source, targets_str = line.split(": ")
        targets = targets_str.split(" ")
        components[source].update(targets)
        for target in targets:
            components[target].add(source)

    occurrences = defaultdict(lambda: 0)
    for part in components.keys():
        print(part)
        shortest_paths = find_shortest_paths(components, part)
        count_occurrences(occurrences, shortest_paths)

    top_three = get_top_items(occurrences, 3)

    components_cut = copy.deepcopy(components)
    for wire in top_three:
        part1, part2 = wire.split("_")
        components_cut[part1].remove(part2)
        components_cut[part2].remove(part1)

    group1 = find_shortest_paths(components_cut, list(components_cut.keys())[0])
    size1 = len(group1.keys())

    return size1 * (len(components) - size1), 0


def find_shortest_paths(components, start):
    the_max = len(components)
    shortest_paths = {start: [start]}
    to_check = [start]
    while to_check:
        curr = to_check.pop(0)
        curr_len = len(shortest_paths[curr]) if curr in shortest_paths else the_max
        targets = components[curr]
        for target in targets:
            if target in shortest_paths:
                if curr_len > len(shortest_paths[target]) + 1:
                    shortest_paths[curr] = shortest_paths[target] + [curr]
                    for target_again in targets:
                        if target_again != target and target_again not in to_check:
                            to_check.append(target_again)
            elif target not in to_check:
                to_check.append(target)
    return shortest_paths


def count_occurrences(occurrences, shortest_paths):
    for shortest_path in shortest_paths.values():
        for i in range(0, len(shortest_path) - 1):
            part1 = shortest_path[i]
            part2 = shortest_path[i+1]
            if part1 < part2:
                key = f"{part1}_{part2}"
            else:
                key = f"{part2}_{part1}"
            occurrences[key] += 1


def get_top_items(my_dict, num_items):
    top_items = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)[:num_items]
    return [item[0] for item in top_items]


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
