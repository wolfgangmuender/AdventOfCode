import os
import time
from functools import cache

TEST_SOLUTION1 = 126384
TEST_SOLUTION2 = 154115708116294

BUTTONS_NUM = {"A": [2, 3], "0": [1, 3], "1": [0, 2], "2": [1, 2], "3": [2, 2], "4": [0, 1], "5": [1, 1], "6": [2, 1], "7": [0, 0], "8": [1, 0], "9": [2, 0]}
BUTTONS_ARROW = {"A": [2, 0], "^": [1, 0], "<": [0, 1], "v": [1, 1], ">": [2, 1]}


def solve(puzzle_input):
    codes = []
    for line in puzzle_input:
        codes.append(line)

    total_complexity1 = 0
    total_complexity2 = 0
    for code in codes:
        moves = []
        pos = [2, 3]
        for b in code:
            target = BUTTONS_NUM[b]
            moves += get_moves_num(pos, target)
            pos = target

        num_moves1 = 0
        num_moves2 = 0
        pos = [2, 0]
        for move in moves:
            target = BUTTONS_ARROW[move]
            num_moves1 += execute_by_robots(pos[0], pos[1], target[0], target[1], 2)
            num_moves2 += execute_by_robots(pos[0], pos[1], target[0], target[1], 25)
            pos = target

        total_complexity1 += num_moves1 * int(code[:-1])
        total_complexity2 += num_moves2 * int(code[:-1])

    return total_complexity1, total_complexity2


@cache
def execute_by_robots(xp, yp, xt, yt, num_robots):
    if num_robots == 0:
        return 1

    num_moves = 0
    pos = [2, 0]
    for move in get_moves_arrow(xp, yp, xt, yt):
        target = BUTTONS_ARROW[move]
        num_moves += execute_by_robots(pos[0], pos[1], target[0], target[1], num_robots - 1)
        pos = target
    return num_moves


def get_moves_num(pos, target):
    moves = []

    xp, yp = pos
    xt, yt = target
    if yp == 3 and xt == 0:
        for i in range(0, yp - yt):
            moves.append("^")
        for i in range(0, xp - xt):
            moves.append("<")
    elif xp == 0 and yt == 3:
        for i in range(0, xt - xp):
            moves.append(">")
        for i in range(0, yt - yp):
            moves.append("v")
    else:
        for i in range(0, xp - xt):
            moves.append("<")
        for i in range(0, yp - yt):
            moves.append("^")
        for i in range(0, yt - yp):
            moves.append("v")
        for i in range(0, xt - xp):
            moves.append(">")
    moves.append("A")

    return moves


@cache
def get_moves_arrow(xp, yp, xt, yt):
    moves = []
    if yp == 0 and xt == 0:
        for i in range(0, yt - yp):
            moves.append("v")
        for i in range(0, xp - xt):
            moves.append("<")
    elif xp == 0 and yt == 0:
        for i in range(0, xt - xp):
            moves.append(">")
        for i in range(0, yp - yt):
            moves.append("^")
    else:
        for i in range(0, xp - xt):
            moves.append("<")
        for i in range(0, yp - yt):
            moves.append("^")
        for i in range(0, yt - yp):
            moves.append("v")
        for i in range(0, xt - xp):
            moves.append(">")
    moves.append("A")

    return moves


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
