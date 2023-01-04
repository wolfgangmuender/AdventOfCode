import os
import time

from utils import input_to_int_list

TEST_SOLUTION1 = 18
TEST_SOLUTION2 = 9


def solve(puzzle_input):
    rows = []
    for line in puzzle_input:
        rows.append(input_to_int_list(line, "	"))

    solution1 = 0
    for row in rows:
        solution1 += max(row) - min(row)

    solution2 = 0
    for row in rows:
        sorted_row = sorted(row, reverse=True)
        for i in range(0, len(sorted_row)):
            for j in range(i+1, len(sorted_row)):
                if sorted_row[i] % sorted_row[j] == 0:
                    solution2 += int(sorted_row[i] / sorted_row[j])
                    break

    return solution1, solution2


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    if os.path.isfile(test_input_file):
        with open(test_input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
        if solution1 != TEST_SOLUTION1:
            print(f"Solution 1 '{solution1}' not correct for test input")
            return
        if solution2 != TEST_SOLUTION2:
            print(f"Solution 2 '{solution2}' not correct for test input")
            return
        end = time.time()
        print_diff(end - start)
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
        print_diff(end - start)
    else:
        open(input_file, 'a').close()


def print_diff(diff):
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))


if __name__ == "__main__":
    main()
