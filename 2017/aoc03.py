import math
import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 31
TEST_SOLUTION2 = 1968


def solve(puzzle_input):
    target = int(puzzle_input[0])

    rect_length = math.ceil(math.sqrt(target))
    if rect_length % 2 == 0:
        rect_length += 1
    if rect_length * rect_length == target:
        solution1 = rect_length - 1
    else:
        max_extent = int((rect_length - 1) / 2)

        curr = (rect_length - 2) ** 2
        pos = [max_extent - 1, -max_extent + 1]
        go_round(curr, target, pos, max_extent, {}, False)

        solution1 = abs(pos[0]) + abs(pos[1])

    curr = 1
    pos = [0, 0]
    store = defaultdict(lambda: 0)
    store[get_key(pos)] = curr
    max_extent = 0
    while curr < target:
        max_extent += 1
        curr = go_round(curr, target, pos, max_extent, store, True)
    solution2 = curr

    return solution1, solution2


def go_round(curr, target, pos, max_extent, store, use_sum):
    if curr < target:
        pos[0] += 1
        if use_sum:
            curr = 0
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if x != 0 or y != 0:
                        curr += store[get_key([pos[0] + x, pos[1] + y])]
        else:
            curr += 1
        store[get_key(pos)] = curr

    while curr < target:
        if pos[1] < max_extent:
            pos[1] += 1
            if use_sum:
                curr = 0
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x != 0 or y != 0:
                            curr += store[get_key([pos[0] + x, pos[1] + y])]
            else:
                curr += 1
            store[get_key(pos)] = curr
        else:
            break

    while curr < target:
        if pos[0] > -max_extent:
            pos[0] -= 1
            if use_sum:
                curr = 0
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x != 0 or y != 0:
                            curr += store[get_key([pos[0] + x, pos[1] + y])]
            else:
                curr += 1
            store[get_key(pos)] = curr
        else:
            break

    while curr < target:
        if pos[1] > -max_extent:
            pos[1] -= 1
            if use_sum:
                curr = 0
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x != 0 or y != 0:
                            curr += store[get_key([pos[0] + x, pos[1] + y])]
            else:
                curr += 1
            store[get_key(pos)] = curr
        else:
            break

    while curr < target:
        if pos[0] < max_extent:
            pos[0] += 1
            if use_sum:
                curr = 0
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x != 0 or y != 0:
                            curr += store[get_key([pos[0] + x, pos[1] + y])]
            else:
                curr += 1
            store[get_key(pos)] = curr
        else:
            break

    return curr


def get_key(pos):
    return f"{pos[0]}_{pos[1]}"


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
        print_diff(end - start)
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
        print_diff(end - start)
    else:
        open(input_file, 'a').close()


def print_diff(diff):
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))


if __name__ == "__main__":
    main()
