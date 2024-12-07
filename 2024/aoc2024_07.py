import os
import time

TEST_SOLUTION1 = 3749
TEST_SOLUTION2 = 11387


def solve(puzzle_input):
    calibrations = []
    for line in puzzle_input:
        test_value, numbers = line.split(": ")
        calibrations.append([int(test_value), [int(n) for n in numbers.split(" ")]])

    total_calibration_result = 0
    for equation in calibrations:
        if equation[0] in get_all_combinations(equation[1]):
            total_calibration_result += equation[0]

    total_calibration_result2 = 0
    for equation in calibrations:
        if equation[0] in get_all_combinations2(equation[1]):
            total_calibration_result2 += equation[0]

    return total_calibration_result, total_calibration_result2

def get_all_combinations(numbers):
    if len(numbers) == 2:
        return [numbers[0] + numbers[1], numbers[0] * numbers[1]]

    curr = numbers[-1]
    sub_combinations = get_all_combinations(numbers[:-1])

    return [n + curr for n in sub_combinations] + [n * curr for n in sub_combinations]

def get_all_combinations2(numbers):
    if len(numbers) == 2:
        return [numbers[0] + numbers[1], numbers[0] * numbers[1], concat(numbers[0], numbers[1])]

    curr = numbers[-1]
    sub_combinations = get_all_combinations2(numbers[:-1])

    return [n + curr for n in sub_combinations] + [n * curr for n in sub_combinations] + [concat(n, curr) for n in sub_combinations]


def concat(num1, num2):
    return int(f"{num1}{num2}")


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
