import os
import time
from math import ceil

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 136
TEST_SOLUTION2 = 64


def solve(puzzle_input):
    rocks = PseudoMatrix()
    for line in puzzle_input:
        rocks.append_row(line)

    rocks1 = rocks.copy()
    for x, y in rocks1.iter():
        if rocks1[x, y] == "O":
            move_rock(rocks1, x, y, 0)

    total_cycles = 1000000000
    total_loads = []
    repeating = None

    curr_rocks = rocks.copy()
    while len(total_loads) < total_cycles:
        # North
        for x, y in curr_rocks.iter():
            if curr_rocks[x, y] == "O":
                move_rock(curr_rocks, x, y, 0)
        # West
        for x, y in curr_rocks.iter():
            if curr_rocks[x, y] == "O":
                move_rock(curr_rocks, x, y, 3)
        # South
        for x in curr_rocks.iter_x():
            for y in curr_rocks.iter_y(direction=-1):
                if curr_rocks[x, y] == "O":
                    move_rock(curr_rocks, x, y, 2)
        # East
        for x in curr_rocks.iter_x(direction=-1):
            for y in curr_rocks.iter_y():
                if curr_rocks[x, y] == "O":
                    move_rock(curr_rocks, x, y, 1)

        curr_total_load = calculate_total_load(curr_rocks)
        total_loads.append(curr_total_load)

        repeating = check_for_repeating_pattern(total_loads)
        if repeating:
            break

    repeating_len = len(repeating)
    remaining_cycles = (total_cycles - len(total_loads)) % repeating_len
    final_load = repeating[remaining_cycles-1]

    return calculate_total_load(rocks1), final_load


# 0=N,1=E,2=S,3=W
def move_rock(rocks, xs, ys, direction):
    if direction == 0:
        y = ys
        while y > 0 and rocks[xs, y - 1] == ".":
            y -= 1
        rocks[xs, ys] = "."
        rocks[xs, y] = "O"
    elif direction == 1:
        x = xs
        while x < rocks.x_range[1] and rocks[x + 1, ys] == ".":
            x += 1
        rocks[xs, ys] = "."
        rocks[x, ys] = "O"
    elif direction == 2:
        y = ys
        while y < rocks.y_range[1] and rocks[xs, y + 1] == ".":
            y += 1
        rocks[xs, ys] = "."
        rocks[xs, y] = "O"
    elif direction == 3:
        x = xs
        while x > 0 and rocks[x - 1, ys] == ".":
            x -= 1
        rocks[xs, ys] = "."
        rocks[x, ys] = "O"
    else:
        raise Exception("Whoooot?")


def calculate_total_load(rocks):
    total_load = 0
    for x, y in rocks.iter():
        if rocks[x, y] == "O":
            total_load += rocks.y_range[1] + 1 - y
    return total_load


def check_for_repeating_pattern(total_loads):
    n = len(total_loads)
    for i in range(2, ceil(n / 3)):
        if 3 * i > n:
            return None

        if check_repeating(total_loads, n, i):
            return total_loads[(n - i):]

    return None


def check_repeating(total_loads, n, i):
    for j in range(0, i):
        a = total_loads[n - 3 * i + j]
        b = total_loads[n - 2 * i + j]
        c = total_loads[n - i + j]
        if a != b or a != c or b != c:
            return False
    return True


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
