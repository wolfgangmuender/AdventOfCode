import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 4
TEST_SOLUTION2 = 3


def solve(puzzle_input):
    container_sizes = [int(line) for line in puzzle_input]
    liters = 150 if len(container_sizes) > 5 else 25

    combinations = find_combinations(container_sizes, liters)
    min_number = min(combinations.keys())

    return sum(combinations.values()), combinations[min_number]


def find_combinations(container_sizes, liters):
    if liters == 0:
        return {0: 1}
    if len(container_sizes) == 0:
        return {}

    combinations = defaultdict(lambda: 0)
    for i in range(0, len(container_sizes)):
        container_size = container_sizes[i]
        if container_size <= liters:
            sub_combinations = find_combinations(container_sizes[i+1:], liters-container_size)
            for num_containers, num_combinations in sub_combinations.items():
                combinations[num_containers+1] += num_combinations
    return combinations



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
