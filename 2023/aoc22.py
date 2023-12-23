import os
import time
from collections import defaultdict
from copy import deepcopy

TEST_SOLUTION1 = 5
TEST_SOLUTION2 = 7


def solve(puzzle_input):
    bricks = []
    i = 0
    for line in puzzle_input:
        i += 1
        brick1, brick2 = line.split("~")
        bricks.append([i, [int(b) for b in brick1.split(",")], [int(b) for b in brick2.split(",")]])

    curr_bricks = deepcopy(bricks)
    curr_bricks.sort(key=lambda x: x[1][2])
    z_map = defaultdict(list)
    for curr_brick in curr_bricks:
        add_to_z_map(z_map, curr_brick)
        while curr_brick[1][2] > 1 and not get_bricks(z_map, curr_brick, -1):
            remove_from_z_map(z_map, curr_brick)
            curr_brick[1][2] -= 1
            curr_brick[2][2] -= 1
            add_to_z_map(z_map, curr_brick)

    brick_hierarchy = {}
    for curr_brick in curr_bricks:
        if curr_brick[1][2] == 1:
            brick_hierarchy[curr_brick[0]] = [0]
        else:
            brick_hierarchy[curr_brick[0]] = [brick[0] for brick in get_bricks(z_map, curr_brick, -1)]

    blocked_bricks = {bricks_below[0] for bricks_below in brick_hierarchy.values() if len(bricks_below) == 1 and bricks_below[0] != 0}

    total_falling_bricks = 0
    for curr_brick in curr_bricks:
        falling_bricks = 0
        curr_brick_hierarchy = deepcopy(brick_hierarchy)
        unsupported_brick_nums = {curr_brick[0]}
        while unsupported_brick_nums:
            falling_bricks += 1
            unsupported_brick_num = unsupported_brick_nums.pop()
            remove_brick(curr_brick_hierarchy, unsupported_brick_num)
            unsupported_brick_nums.update(get_unsupported_bricks(curr_brick_hierarchy))
        total_falling_bricks += falling_bricks - 1

    return len(bricks) - len(blocked_bricks), total_falling_bricks


def get_bricks(z_map, curr_brick, zd):
    x1 = curr_brick[1][0]
    x2 = curr_brick[2][0]
    y1 = curr_brick[1][1]
    y2 = curr_brick[2][1]
    z = curr_brick[1][2] if zd < 0 else curr_brick[2][2]
    bricks_below = []
    for brick in z_map[z + zd]:
        if x1 <= brick[2][0] and brick[1][0] <= x2 and y1 <= brick[2][1] and brick[1][1] <= y2:
            bricks_below.append(brick)
    return bricks_below


def remove_from_z_map(z_map, curr_brick):
    for z in range(curr_brick[1][2], curr_brick[2][2] + 1):
        z_map[z].remove(curr_brick)


def add_to_z_map(z_map, curr_brick):
    for z in range(curr_brick[1][2], curr_brick[2][2] + 1):
        z_map[z].append(curr_brick)


def remove_brick(brick_hierarchy, unsupported_brick_num):
    del brick_hierarchy[unsupported_brick_num]
    for brick_num in brick_hierarchy:
        if unsupported_brick_num in brick_hierarchy[brick_num]:
            brick_hierarchy[brick_num].remove(unsupported_brick_num)


def get_unsupported_bricks(brick_hierarchy):
    return [brick_num for brick_num in brick_hierarchy if not brick_hierarchy[brick_num]]


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
