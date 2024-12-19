import os
import time

TEST_SOLUTION1 = 6
TEST_SOLUTION2 = 16


def solve(puzzle_input):
    towels = []
    designs = []
    for line in puzzle_input:
        if "," in line:
            towels = line.split(", ")
        elif line:
            designs.append(line)

    num_possible = 0
    total_combinations = 0
    cache = {}
    for design in designs:
        towel_combinations = match_recursively(design, towels, cache)
        if towel_combinations > 0:
            num_possible += 1
            total_combinations += towel_combinations

    return num_possible, total_combinations


def match_recursively(design, towels, cache):
    if design not in cache:
        num_towel_combinations = 0
        for towel in towels:
            if design == towel:
                num_towel_combinations += 1
            elif design.startswith(towel):
                num_towel_combinations += match_recursively(design.replace(towel, "", 1), towels, cache)
        cache[design] = num_towel_combinations

    return cache[design]


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
