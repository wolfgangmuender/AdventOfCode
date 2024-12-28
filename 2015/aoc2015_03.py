import os
import time

TEST_SOLUTION1 = 4
TEST_SOLUTION2 = 3

DIRECTIONS = {"^": [0, -1], "v": [0, 1], ">": [1, 0], "<": [-1, 0]}


def solve(puzzle_input):
    moves = [c for c in puzzle_input[0]]

    start = tuple([0, 0])
    visited1 = {start}
    x, y = start
    for move in moves:
        xd, yd = DIRECTIONS[move]
        x += xd
        y += yd
        visited1.add(tuple([x, y]))

    start = tuple([0, 0])
    visited2 = {start}
    xs, ys = start
    xr, yr = start
    is_santa = True
    for move in moves:
        xd, yd = DIRECTIONS[move]
        if is_santa:
            xs += xd
            ys += yd
            visited2.add(tuple([xs, ys]))
        else:
            xr += xd
            yr += yd
            visited2.add(tuple([xr, yr]))
        is_santa = not is_santa

    return len(visited1), len(visited2)


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
