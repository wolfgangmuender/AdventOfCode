import os
import time
from copy import copy

import math

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 12
TEST_SOLUTION2 = 0


def solve(puzzle_input):
    ps = []
    vs = []
    for line in puzzle_input:
        pstring, vstring = line.replace("p=", "").replace("v=", "").split(" ")
        ps.append(tuple([int(n) for n in pstring.split(",")]))
        vs.append(tuple([int(n) for n in vstring.split(",")]))

    w = 11 if len(ps) == 12 else 101
    h = 7 if len(ps) == 12 else 103

    num_q = [0, 0, 0, 0]
    for i in range(0, len(ps)):
        x, y = ps[i]
        vx, vy = vs[i]
        for n in range(0, 100):
            x = (x + vx) % w
            y = (y + vy) % h

        xm = w // 2
        ym = h // 2
        if 0 <= x < xm and 0 <= y < ym:
            num_q[0] += 1
        elif 0 <= x < xm and ym < y <= h:
            num_q[1] += 1
        elif xm < x <= w and 0 <= y < ym:
            num_q[2] += 1
        elif xm < x <= w and ym < y <= h:
            num_q[3] += 1

    p_curr = copy(ps)
    num = 0
    if len(ps) > 12:
        while not check_for_tree(p_curr):
            for i in range(0, len(p_curr)):
                x, y = p_curr[i]
                vx, vy = vs[i]
                x = (x + vx) % w
                y = (y + vy) % h
                p_curr[i] = tuple([x, y])
            num += 1
            print(num)

        r = PseudoMatrix(".")
        for p in p_curr:
            x, y = p
            r[x, y] = "#"
        r.print()

    return math.prod(num_q), num


def check_for_tree(ps):
    for p in ps:
        x, y = p
        check = [tuple([x + i, y - i]) in ps for i in range(0, 10)]
        if all(check):
            return True
    return False


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
