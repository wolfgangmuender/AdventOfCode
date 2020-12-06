import os
import time
from math import floor, ceil

TEST_SOLUTION1 = 357
TEST_SOLUTION2 = None


def solve(puzzle_input):
    seat_ids = []
    for line in puzzle_input:
        row_min = 0
        row_max = 127
        seat_min = 0
        seat_max = 7
        for c in line:
            if c == "F":
                row_max = floor((row_min + row_max) / 2)
            elif c == "B":
                row_min = ceil((row_min + row_max) / 2)
            elif c == "L":
                seat_max = floor((seat_min + seat_max) / 2)
            elif c == "R":
                seat_min = ceil((seat_min + seat_max) / 2)
            else:
                raise Exception("Whoot?")
        seat_ids.append(row_min * 8 + seat_min)

    seat_id = None
    for i in range(min(seat_ids), max(seat_ids)):
        if i not in seat_ids:
            seat_id = i
            break

    return max(seat_ids), seat_id


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
