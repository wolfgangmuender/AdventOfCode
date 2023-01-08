import os
import time
from copy import copy

TEST_SOLUTION1 = 5
TEST_SOLUTION2 = 4


def solve(puzzle_input):
    initial_memory_banks = [int(c) for c in puzzle_input[0].split(" ")]

    memory_banks = []
    curr = copy(initial_memory_banks)
    while curr not in memory_banks:
        memory_banks.append(curr)

        max_value = max(curr)
        max_index = curr.index(max_value)

        curr = copy(curr)
        curr[max_index] = 0
        curr_index = max_index
        while max_value > 0:
            curr_index = curr_index + 1 if curr_index < (len(curr) - 1) else 0
            curr[curr_index] += 1
            max_value -= 1

    solution1 = len(memory_banks)
    solution2 = len(memory_banks) - memory_banks.index(curr)

    return solution1, solution2



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
