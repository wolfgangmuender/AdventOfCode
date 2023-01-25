import os
import time

TEST_SOLUTION1 = 638


def solve(puzzle_input):
    num_steps = int(puzzle_input[0])

    start, curr = spin(num_steps, 2017)
    solution1 = curr["n"]["v"]

    start, curr = spin(num_steps, 50000000)
    solution2 = start["n"]["v"]

    return solution1, solution2


def spin(num_steps, num_values):
    start = {"v": 0}
    curr = start
    curr["n"] = curr
    for i in range(1, num_values + 1):
        for j in range(0, num_steps):
            curr = curr["n"]
        new = {"v": i, "n": curr["n"]}
        curr["n"] = new

        curr = new

    return start, curr


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
