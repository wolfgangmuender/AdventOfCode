import os
import time
from copy import copy

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 46
TEST_SOLUTION2 = 51


def solve(puzzle_input):
    contraption = PseudoMatrix()
    for line in puzzle_input:
        contraption.append_row(line)

    energized = []
    for y in contraption.iter_y():
        energized.append(energize(contraption, contraption.x_range[0], y, ">"))
        energized.append(energize(contraption, contraption.x_range[1], y, "<"))
    for x in contraption.iter_x():
        energized.append(energize(contraption, x, contraption.y_range[0], "v"))
        energized.append(energize(contraption, x, contraption.y_range[1], "^"))

    return energized[0], max(energized)


def energize(contraption, x, y, direction):
    energized = set()
    visited = []
    beams = [[x, y, direction]]
    while beams:
        curr = beams.pop()
        if curr in visited:
            continue

        visited.append(curr)
        energized.add(f"{curr[0]}_{curr[1]}")
        beams += get_next(contraption, curr)

    return len(energized)


def get_next(contraption, curr):
    x, y, direction = curr
    if direction == "^":
        if contraption[x, y] == "." or contraption[x, y] == "|":
            if y > 0:
                return [[x, y - 1, "^"]]
        elif contraption[x, y] == "-":
            res = []
            if x > 0:
                res.append([x - 1, y, "<"])
            if x < contraption.x_range[1]:
                res.append([x + 1, y, ">"])
            return res
        elif contraption[x, y] == "/":
            if x < contraption.x_range[1]:
                return [[x + 1, y, ">"]]
        elif contraption[x, y] == "\\":
            if x > 0:
                return [[x - 1, y, "<"]]
    elif direction == "v":
        if contraption[x, y] == "." or contraption[x, y] == "|":
            if y < contraption.y_range[1]:
                return [[x, y + 1, "v"]]
        elif contraption[x, y] == "-":
            res = []
            if x > 0:
                res.append([x - 1, y, "<"])
            if x < contraption.x_range[1]:
                res.append([x + 1, y, ">"])
            return res
        elif contraption[x, y] == "/":
            if x > 0:
                return [[x - 1, y, "<"]]
        elif contraption[x, y] == "\\":
            if x < contraption.x_range[1]:
                return [[x + 1, y, ">"]]
    elif direction == ">":
        if contraption[x, y] == "." or contraption[x, y] == "-":
            if x < contraption.x_range[1]:
                return [[x + 1, y, ">"]]
        elif contraption[x, y] == "|":
            res = []
            if y > 0:
                res.append([x, y - 1, "^"])
            if y < contraption.y_range[1]:
                res.append([x, y + 1, "v"])
            return res
        elif contraption[x, y] == "/":
            if y > 0:
                return [[x, y - 1, "^"]]
        elif contraption[x, y] == "\\":
            if y < contraption.y_range[1]:
                return [[x, y + 1, "v"]]
    elif direction == "<":
        if contraption[x, y] == "." or contraption[x, y] == "-":
            if x > 0:
                return [[x - 1, y, "<"]]
        elif contraption[x, y] == "|":
            res = []
            if y > 0:
                res.append([x, y - 1, "^"])
            if y < contraption.y_range[1]:
                res.append([x, y + 1, "v"])
            return res
        elif contraption[x, y] == "/":
            if y < contraption.y_range[1]:
                return [[x, y + 1, "v"]]
        elif contraption[x, y] == "\\":
            if y > 0:
                return [[x, y - 1, "^"]]

    return []


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
