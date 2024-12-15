import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 10092
TEST_SOLUTION2 = 9021

DIRECTIONS = {"^": [0, -1], "v": [0, 1], ">": [1, 0], "<": [-1, 0]}
ENLARGE = {"#": "##", "O": "[]", ".": "..", "@": "@."}


def solve(puzzle_input):
    initial_map = PseudoMatrix()
    moves = []
    is_map = True
    for line in puzzle_input:
        if not line:
            is_map = False
        elif is_map:
            initial_map.append_row(line)
        else:
            moves += [c for c in line]

    the_map = initial_map.copy()
    x, y = get_start(the_map)
    for move in moves:
        xd, yd = DIRECTIONS[move]
        if the_map[x + xd, y + yd] == "#":
            continue
        elif the_map[x + xd, y + yd] == ".":
            the_map[x, y] = "."
            the_map[x + xd, y + yd] = "@"
            x += xd
            y += yd
        elif the_map[x + xd, y + yd] == "O":
            movable_box_length = get_movable_box_length(the_map, x, y, xd, yd)
            if movable_box_length > 0:
                for i in range(movable_box_length + 1, 1, -1):
                    the_map[x + i * xd, y + i * yd] = "O"
                the_map[x + xd, y + yd] = "@"
                the_map[x, y] = "."
                x += xd
                y += yd

    large_map = enlarge_map(initial_map)
    x, y = get_start(large_map)
    for move in moves:
        xd, yd = DIRECTIONS[move]
        if large_map[x + xd, y + yd] == "#":
            continue
        elif large_map[x + xd, y + yd] == ".":
            large_map[x, y] = "."
            large_map[x + xd, y + yd] = "@"
            x += xd
            y += yd
        elif large_map[x + xd, y + yd] == "[" or large_map[x + xd, y + yd] == "]":
            if yd == 0:
                movable_box_length = get_movable_box_length(large_map, x, y, xd, yd)
                if movable_box_length > 0:
                    for i in range(movable_box_length + 1, 1, -1):
                        large_map[x + i * xd, y + i * yd] = large_map[x + (i - 1) * xd, y + (i - 1) * yd]
                    large_map[x + xd, y + yd] = "@"
                    large_map[x, y] = "."
                    x += xd
                    y += yd
            else:
                x, y = move_boxes_vertically(large_map, x, y, yd)

    return get_gps_score(the_map, "O"), get_gps_score(large_map, "[")


def get_start(the_map):
    for x, y in the_map.iter():
        if the_map[x, y] == "@":
            return x, y
    raise Exception("Whoot?")


def enlarge_map(the_map):
    large_map = PseudoMatrix()
    for _, row in the_map.iter_rows():
        new_row = ""
        for c in row:
            new_row += ENLARGE[c]
        large_map.append_row(new_row)
    return large_map


def get_movable_box_length(the_map, x, y, xd, yd):
    check = 2
    while the_map[x + check * xd, y + check * yd] != "#":
        if the_map[x + check * xd, y + check * yd] in ["O", "[", "]"]:
            check += 1
        elif the_map[x + check * xd, y + check * yd] == ".":
            return check - 1
    return 0


def move_boxes_vertically(large_map, x, y, yd):
    boxes_to_check = []
    if large_map[x, y + yd] == "[":
        boxes_to_check.append([x, y + yd])
    else:
        boxes_to_check.append([x - 1, y + yd])
    boxes_to_move = []

    while boxes_to_check:
        xb, yb = boxes_to_check.pop(0)
        boxes_to_move.append([xb, yb])
        if large_map[xb, yb + yd] == "#" or large_map[xb + 1, yb + yd] == "#":
            return x, y
        if large_map[xb, yb + yd] == "[":
            boxes_to_check.append([xb, yb + yd])
        if large_map[xb, yb + yd] == "]":
            boxes_to_check.append([xb - 1, yb + yd])
        if large_map[xb + 1, yb + yd] == "[":
            boxes_to_check.append([xb + 1, yb + yd])

    while boxes_to_move:
        xb, yb = boxes_to_move.pop()
        large_map[xb, yb] = "."
        large_map[xb + 1, yb] = "."
        large_map[xb, yb + yd] = "["
        large_map[xb + 1, yb + yd] = "]"

    large_map[x, y] = "."
    large_map[x, y + yd] = "@"

    return x, y + yd


def get_gps_score(the_map, c):
    gps_score = 0
    for x, y in the_map.iter():
        if the_map[x, y] == c:
            gps_score += 100 * y + x
    return gps_score


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
