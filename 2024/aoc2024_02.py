import os
import time

TEST_SOLUTION1 = 2
TEST_SOLUTION2 = 4


def solve(puzzle_input):
    reports = []
    for line in puzzle_input:
        reports.append([int(l) for l in line.split(" ")])

    num_safe = 0
    for report in reports:
        if is_safe(report, False):
            num_safe += 1

    num_safe_pd = 0
    for report in reports:
        if is_safe(report, True):
            num_safe_pd += 1

    return num_safe, num_safe_pd


def is_safe(report, with_dp):
    is_increasing = all([1 <= report[i + 1] - report[i] <= 3 for i in range(0, len(report) - 1)])
    is_decreasing = all([-3 <= report[i + 1] - report[i] <= -1 for i in range(0, len(report) - 1)])

    if is_increasing or is_decreasing:
        return True

    if with_dp:
        for i in range(0, len(report)):
            if is_safe(report[:i] + report[i+1:], False):
                return True

    return False


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
