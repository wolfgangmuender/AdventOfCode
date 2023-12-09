import math
import os
import time

TEST_SOLUTION1 = 6
TEST_SOLUTION2 = 6


def solve(puzzle_input):
    sequence = [0 if c == "L" else 1 for c in puzzle_input[0]]
    network = {}
    for line in puzzle_input[2:]:
        source, targets = line.split(" = ")
        network[source] = targets[1:-1].split(", ")

    if "AAA" in network.keys():
        curr = "AAA"
        steps1 = 0
        while curr != "ZZZ":
            curr = do_step(network, sequence, curr, steps1)
            steps1 += 1
    else:
        steps1 = 0

    cycles = []
    for node in network.keys():
        if node.endswith("A"):
            steps = 0
            curr = node
            while not curr.endswith("Z"):
                curr = do_step(network, sequence, curr, steps)
                steps += 1
            cycles.append(steps)

    return steps1, lcm_of_list(cycles)


def do_step(network, sequence, curr, steps):
    return network[curr][sequence[steps % len(sequence)]]


def lcm_of_list(numbers):
    current_lcm = numbers[0]
    for number in numbers[1:]:
        current_lcm = lcm(current_lcm, number)

    return current_lcm


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


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
