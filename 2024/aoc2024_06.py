import os
import time
from collections import defaultdict

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 41
TEST_SOLUTION2 = 6

DIRECTIONS = {"^": [0, -1], "v": [0, 1], ">": [1, 0], "<": [-1, 0]}
TURN_RIGHT = {"^": ">", ">": "v", "v": "<", "<": "^"}


def solve(puzzle_input):
    original_map = PseudoMatrix("X")
    for line in puzzle_input:
        original_map.append_row(line)

    xs = None
    ys = None
    ds = None
    for x, y in original_map.iter():
        if original_map[x, y] not in [".", "#"]:
            xs = x
            ys = y
            ds = original_map[x, y]
            break

    first_map = original_map.copy()
    path_positions = set()
    xc = xs
    yc = ys
    dc = ds
    while first_map[xc, yc] != "X":
        path_positions.add(f"{xc},{yc}")
        xc, yc, dc = do_step(first_map, xc, yc, dc)

    num_loops = 0
    for path_position in path_positions:
        xp, yp = [int(n) for n in path_position.split(",")]
        if xp == xs and yp == ys:
            continue

        blocked_map = original_map.copy()
        blocked_map[xp,yp] = "#"
        visited_positions = defaultdict(lambda: 0)
        xc = xs
        yc = ys
        dc = ds
        while blocked_map[xc, yc] != "X" and visited_positions[f"{xc},{yc}"] < 5:
            visited_positions[f"{xc},{yc}"] += 1
            xc, yc, dc = do_step(blocked_map, xc, yc, dc)

        if blocked_map[xc, yc] != "X":
            num_loops += 1

    return len(path_positions), num_loops


def do_step(the_map, xc, yc, direction):
    xd, yd = DIRECTIONS[direction]
    while the_map[xc + xd, yc + yd] == "#":
        direction = TURN_RIGHT[direction]
        xd, yd = DIRECTIONS[direction]

    if the_map[xc + xd, yc + yd] == ".":
        the_map[xc + xd, yc + yd] = direction

    return xc + xd, yc + yd, direction


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
