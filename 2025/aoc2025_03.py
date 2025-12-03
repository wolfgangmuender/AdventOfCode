import os
import time

TEST_SOLUTION1 = 357
TEST_SOLUTION2 = 3121910778619


def solve(puzzle_input):
    batteries = []
    for line in puzzle_input:
        batteries.append([int(n) for n in line])

    total_output_joltage1 = 0
    total_output_joltage2 = 0
    for battery in batteries:
        total_output_joltage1 += get_largest_number(battery, 2)
        total_output_joltage2 += get_largest_number(battery, 12)

    return total_output_joltage1, total_output_joltage2


def get_largest_number(numbers, num):
    if num == 1:
        return max(numbers)

    n = max(numbers[:-(num - 1)])

    return n * (10 ** (num - 1)) + get_largest_number(numbers[numbers.index(n) + 1:], num - 1)


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
