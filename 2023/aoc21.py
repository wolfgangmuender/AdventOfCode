import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 42
TEST_SOLUTION2 = 0


def solve(puzzle_input):
    garden_map = PseudoMatrix()
    for line in puzzle_input:
        garden_map.append_row(line)

    tiles = walk(garden_map)

    return len(tiles), 0


def walk(garden_map):
    middle = int(garden_map.x_range[1] / 2)
    assert garden_map[middle, middle] == "S"
    tiles = [[middle, middle]]
    for i in range(0, 64):
        next_tiles = []
        for tile in tiles:
            for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x = tile[0] + d[0]
                y = tile[1] + d[1]
                if garden_map.is_x_within(x) and garden_map.is_y_within(y) and garden_map[x, y] != "#":
                    if not [x, y] in next_tiles:
                        next_tiles.append([x, y])
        tiles = next_tiles
        print(len(tiles))
    return tiles


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
