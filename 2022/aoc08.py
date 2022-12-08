import math
import os
import time


def main(puzzle_input):
    trees = []
    for line in puzzle_input:
        trees.append([int(h) for h in line])

    width = len(trees[0])
    length = len(trees)

    visibility = _initialise_visibility(trees)
    for col in range(1, width):
        for row in range(1, length):
            if _check_visibility(trees, row, col, -1, 0):
                visibility[row][col] = 1
        for row in range(length-2, 0, -1):
            if _check_visibility(trees, row, col, 1, 0):
                visibility[row][col] = 1
    for row in range(1, length):
        for col in range(1, width):
            if _check_visibility(trees, row, col, 0, -1):
                visibility[row][col] = 1
        for col in range(width-2, 0, -1):
            if _check_visibility(trees, row, col, 0, 1):
                visibility[row][col] = 1

    print("Solution 1: {}".format(sum([sum(row) for row in visibility])))

    scenic_scores = []
    for row in range(0, length):
        scenic_scores.append([])
        for col in range(0, width):
            sc = _count_visible_trees(trees, row, col, 1, 0) * _count_visible_trees(trees, row, col, -1, 0) * _count_visible_trees(trees, row, col, 0, 1) * _count_visible_trees(trees, row, col, 0, -1)
            scenic_scores[row].append(sc)

    print("Solution 2: {}".format(max([max(sc) for sc in scenic_scores])))


def _initialise_visibility(trees):
    width = len(trees[0])
    length = len(trees)
    visibility = [[0]*width for _ in trees]
    visibility[0] = [1]*length
    visibility[-1] = [1]*length
    for row in visibility:
        row[0] = 1
        row[-1] = 1
    return visibility


def _check_visibility(trees, row, col, diff_row, diff_col):
    r = row + diff_row
    c = col + diff_col
    while 0 <= r < len(trees) and 0 <= c < len(trees[r]):
        if trees[row][col] <= trees[r][c]:
            return False
        r += diff_row
        c += diff_col
    return True


def _count_visible_trees(trees, row, col, diff_row, diff_col):
    num_trees = 0
    r = row + diff_row
    c = col + diff_col
    while 0 <= r < len(trees) and 0 <= c < len(trees[r]):
        num_trees += 1
        if trees[row][col] <= trees[r][c]:
            break
        r += diff_row
        c += diff_col
    return num_trees


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
