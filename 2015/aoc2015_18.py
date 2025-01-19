import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 4
TEST_SOLUTION2 = 14


def solve(puzzle_input):
    initial_state = PseudoMatrix()
    for line in puzzle_input:
        initial_state.append_row(line)

    num_steps = 100 if initial_state.get_width() > 6 else 4

    curr_correct = initial_state
    for i in range(0, num_steps):
        next_state = curr_correct.copy()
        for x, y in curr_correct.iter():
            num_lights = 0
            for xn, yn in curr_correct.iter_direct_neighbours(x, y, True):
                if curr_correct[xn, yn] == "#":
                    num_lights += 1
            if curr_correct[x, y] == "#":
                if num_lights not in [2, 3]:
                    next_state[x, y] = "."
            if curr_correct[x, y] == ".":
                if num_lights == 3:
                    next_state[x, y] = "#"

        curr_correct = next_state

    curr_stuck = initial_state
    for i in range(0, num_steps):
        next_state = curr_stuck.copy()
        for x, y in curr_stuck.iter():
            if [x, y] in [[0, 0], [curr_stuck.x_range[1], 0], [0, curr_stuck.y_range[1]], [curr_stuck.x_range[1], curr_stuck.y_range[1]]]:
                next_state[x, y] = "#"
                continue

            num_lights = 0
            for xn, yn in curr_stuck.iter_direct_neighbours(x, y, True):
                if curr_stuck[xn, yn] == "#":
                    num_lights += 1
            if curr_stuck[x, y] == "#":
                if num_lights not in [2, 3]:
                    next_state[x, y] = "."
            if curr_stuck[x, y] == ".":
                if num_lights == 3:
                    next_state[x, y] = "#"

        curr_stuck = next_state

    return curr_correct.count("#"), curr_stuck.count("#")


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
