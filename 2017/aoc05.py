import os
import time
from copy import copy

TEST_SOLUTION1 = 5
TEST_SOLUTION2 = 10


def solve(puzzle_input):
    jump_offsets = [int(line) for line in puzzle_input]

    jump_offsets1 = copy(jump_offsets)

    step1 = 0
    pos = 0
    while 0 <= pos < len(jump_offsets1):
        step1 += 1
        old_pos = pos
        pos += jump_offsets1[old_pos]
        jump_offsets1[old_pos] += 1

    jump_offsets2 = copy(jump_offsets)

    step2 = 0
    pos = 0
    while 0 <= pos < len(jump_offsets2):
        step2 += 1
        old_pos = pos
        pos += jump_offsets2[old_pos]
        if jump_offsets2[old_pos] >= 3:
            jump_offsets2[old_pos] -= 1
        else:
            jump_offsets2[old_pos] += 1

    return step1, step2


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
