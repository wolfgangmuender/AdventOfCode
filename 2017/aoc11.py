import os
import time

TEST_SOLUTION1 = 3
TEST_SOLUTION2 = 3


def solve(puzzle_input):
    steps = puzzle_input[0].split(",")

    steps_to_reach_position = []

    x, y = 0, 0
    for step in steps:
        if step == "n":
            y += 1
        elif step == "nw":
            x -= 1
            y += 0.5
        elif step == "ne":
            x += 1
            y += 0.5
        elif step == "sw":
            x -= 1
            y -= 0.5
        elif step == "se":
            x += 1
            y -= 0.5
        elif step == "s":
            y -= 1

        steps_to_reach_position.append(get_steps_to_reach_position(x, y))

    return steps_to_reach_position[-1], max(steps_to_reach_position)


def get_steps_to_reach_position(x, y):
    x_steps = abs(x)
    if x_steps * 0.5 >= abs(y):
        y_steps = 0
    else:
        y_steps = int(abs(y) - x_steps * 0.5)

    return x_steps + y_steps


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
