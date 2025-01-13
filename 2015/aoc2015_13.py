import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 330
TEST_SOLUTION2 = 286


def solve(puzzle_input):
    names = set()
    relations = defaultdict(lambda: 0)
    for line in puzzle_input:
        name1, remainder = line.split(" would ")
        delta_string, name2 = remainder.split(" happiness units by sitting next to ")
        name2 = name2[:-1]
        if delta_string.startswith("gain"):
            delta = int(delta_string[5:])
        elif delta_string.startswith("lose"):
            delta = -int(delta_string[5:])
        else:
            raise Exception("Whoot?")
        names.add(name1)
        names.add(name2)
        relations[key(name1, name2)] = delta

    combinations = get_combinations(names)
    max_total_delta1 = None
    for combination in combinations:
        total_delta = get_total_delta(combination, relations)
        max_total_delta1 = total_delta if not max_total_delta1 or total_delta > max_total_delta1 else max_total_delta1

    names_and_me = names.union({"Me"})
    combinations = get_combinations(names_and_me)
    max_total_delta2 = None
    for combination in combinations:
        total_delta = get_total_delta(combination, relations)
        max_total_delta2 = total_delta if not max_total_delta2 or total_delta > max_total_delta2 else max_total_delta2

    return max_total_delta1, max_total_delta2


def get_combinations(names):
    combinations = []
    for name in names:
        remaining_names = names - {name}
        if remaining_names:
            sub_combinations = get_combinations(remaining_names)
            for sub_combination in sub_combinations:
                combinations.append([name] + sub_combination)
        else:
            combinations.append([name])
    return combinations


def get_total_delta(combination, relations):
    total_delta = 0
    for i in range(0, len(combination)):
        if i < len(combination) - 1:
            total_delta += relations[key(combination[i], combination[i + 1])]
            total_delta += relations[key(combination[i + 1], combination[i])]
        else:
            total_delta += relations[key(combination[i], combination[0])]
            total_delta += relations[key(combination[0], combination[i])]
    return total_delta


def key(name1, name2):
    return tuple([name1, name2])


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
