import os
import time

TEST_SOLUTION1 = 24
TEST_SOLUTION2 = 10


def solve(puzzle_input):
    scanners = {}
    for line in puzzle_input:
        s_depth, s_range = line.split(": ")
        scanners[int(s_depth)] = int(s_range)

    severity_0 = get_severity(scanners, 0, False)

    start = 0
    while True:
        try:
            get_severity(scanners, start, True)
            break
        except StopIteration:
            start += 1

    return severity_0, start


def get_severity(scanners, start, break_on_caught):
    severity = 0
    for s_depth, s_range in scanners.items():
        if (start + s_depth) % (2 * (s_range - 1)) == 0:
            if break_on_caught:
                raise StopIteration()
            severity += s_depth * s_range
    return severity


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    if os.path.isfile(test_input_file):
        with open(test_input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
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
