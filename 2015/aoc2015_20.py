import math
import os
import time

TEST_SOLUTION1 = 4
TEST_SOLUTION2 = 4


def solve(puzzle_input):
    num_presents = int(puzzle_input[0])

    i = 0
    house_number_1 = None
    house_number_2 = None
    while not house_number_1 or not house_number_2:
        divisors = get_divisors(i)
        if not house_number_1 and sum(divisors) * 10 >= num_presents:
            house_number_1 = i
        if not house_number_2 and sum(divisor for divisor in divisors if i / divisor <= 50) * 11 >= num_presents:
            house_number_2 = i
        i += 1

    return house_number_1, house_number_2


def get_divisors(house_number):
    small_divisors = [i for i in range(1, int(math.sqrt(house_number)) + 1) if house_number % i == 0]
    large_divisors = [house_number / d for d in small_divisors if house_number != d * d]
    return small_divisors + large_divisors


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
