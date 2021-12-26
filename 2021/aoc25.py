import os
import time
from copy import deepcopy


def main(puzzle_input):
    sea_cucumbers_initial = {}
    y_size = len(puzzle_input)
    x_size = len(puzzle_input[0])
    for y in range(0, y_size):
        sea_cucumbers_initial[y] = {}
        for x in range(0, x_size):
            sea_cucumbers_initial[y][x] = puzzle_input[y][x]

    steps = 0
    sea_cucumbers = deepcopy(sea_cucumbers_initial)
    while steps == 0 or is_moving:
        steps += 1
        is_moving = False

        sea_cucumbers_static = deepcopy(sea_cucumbers)
        for y in range(0, y_size):
            for x in range(0, x_size):
                x1 = (x + 1) % x_size
                if sea_cucumbers_static[y][x] == ">" and sea_cucumbers_static[y][x1] == ".":
                    sea_cucumbers[y][x] = "."
                    sea_cucumbers[y][x1] = ">"
                    is_moving = True

        sea_cucumbers_static = deepcopy(sea_cucumbers)
        for y in range(0, y_size):
            for x in range(0, x_size):
                y1 = (y + 1) % y_size
                if sea_cucumbers_static[y][x] == "v" and sea_cucumbers_static[y1][x] == ".":
                    sea_cucumbers[y][x] = "."
                    sea_cucumbers[y1][x] = "v"
                    is_moving = True

    print("Solution 1: the first step on which no sea cucumbers move is {}".format(steps))


if __name__ == "__main__":
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    main(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))
