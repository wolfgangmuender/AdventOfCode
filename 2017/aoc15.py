import os
import time

TEST_SOLUTION1 = 588
TEST_SOLUTION2 = 309


def solve(puzzle_input):
    start1 = int(puzzle_input[0].replace("Generator A starts with ", ""))
    start2 = int(puzzle_input[1].replace("Generator B starts with ", ""))

    factor1 = 16807
    factor2 = 48271

    divider = 2147483647

    num_matches = 0
    count = 0
    curr1 = start1
    curr2 = start2
    while count < 40000000:
        if count % 100000 == 0:
            print(count)

        curr1 = curr1 * factor1 % divider
        curr2 = curr2 * factor2 % divider

        num_matches += compare_hexes(curr1, curr2)

        count += 1

    num_matches_picky = 0
    count = 0
    curr1 = start1
    curr2 = start2
    while count < 5000000:
        if count % 100000 == 0:
            print(count)

        curr1 = get_next_value(curr1, factor1, divider, 4)
        curr2 = get_next_value(curr2, factor2, divider, 8)
        num_matches_picky += compare_hexes(curr1, curr2)
        count += 1

    return num_matches, num_matches_picky


def get_next_value(curr, factor, divider, the_mod):
    while True:
        curr = curr * factor % divider
        if curr % the_mod == 0:
            return curr


def compare_hexes(curr1, curr2):
    hex1 = bin(curr1)[2:].rjust(16, "0")
    hex2 = bin(curr2)[2:].rjust(16, "0")

    return 1 if hex1[-16:] == hex2[-16:] else 0


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
