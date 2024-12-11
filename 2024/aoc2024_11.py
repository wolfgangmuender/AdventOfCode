import os
import time
from copy import copy
from functools import cache

TEST_SOLUTION1 = 55312
TEST_SOLUTION2 = 65601038650482


def solve(puzzle_input):
    stones_initial = [int(n) for n in puzzle_input[0].split(" ")]

    return get_total_num_stones(stones_initial, 25), get_total_num_stones(stones_initial, 75)


def get_total_num_stones(stones, num_blinks):
    return sum([get_num_stones(stone, num_blinks) for stone in stones])


@cache
def get_num_stones(stone, num_blinks):
    if num_blinks == 0:
        return 1
    else:
        return sum([get_num_stones(blinked_stone, num_blinks - 1) for blinked_stone in apply_rules(stone)])


def apply_rules(stone):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        stone_string = str(stone)
        return [int(stone_string[:len(stone_string) // 2]), int(stone_string[len(stone_string) // 2:])]
    else:
        return [stone * 2024]


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
