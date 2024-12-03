import os
import re
import time
from copy import copy

TEST_SOLUTION1 = 161
TEST_SOLUTION2 = 48


def solve(puzzle_input):
    memory = copy(puzzle_input)

    pattern_mul = r"mul\(\d+,\d+\)"
    pattern_do = r"do\(\)"
    pattern_dont = r"don\'t\(\)"

    is_enabled = True
    total_sum1 = 0
    total_sum2 = 0
    for line in memory:
        matches = {}
        add_matches(matches, line, pattern_mul)
        add_matches(matches, line, pattern_do)
        add_matches(matches, line, pattern_dont)

        for i in sorted(matches.keys()):
            match = matches[i]
            if match.startswith("mul"):
                num1, num2 = match.replace("mul(", "").replace(")", "").split(",")
                total_sum1 += int(num1) * int(num2)
                if is_enabled:
                    total_sum2 += int(num1) * int(num2)
            elif match.startswith("don"):
                is_enabled = False
            elif match.startswith("do"):
                is_enabled = True

    return total_sum1, total_sum2

def add_matches(all_matches, line, pattern):
    matches = re.finditer(pattern, line)
    for match in matches:
        all_matches[match.start()] = match.group()


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
