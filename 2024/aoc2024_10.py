import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 36
TEST_SOLUTION2 = 81


def solve(puzzle_input):
    the_map = PseudoMatrix(-1)
    for line in puzzle_input:
        the_map.append_row([int(n) for n in line])

    the_map.print()

    total_trailhead_score = 0
    total_trailhead_rating = 0
    for x, y in the_map.iter():
        if the_map[x, y] == 0:
            trailhead_score, trailhead_rating = get_trailhead_score_and_rating(the_map, x, y)
            total_trailhead_score += trailhead_score
            total_trailhead_rating += trailhead_rating

    return total_trailhead_score, total_trailhead_rating


def get_trailhead_score_and_rating(the_map, xc, yc):
    paths = get_paths(the_map, xc, yc, 0)
    return len({tuple(path[-1]) for path in paths}), len(paths)


def get_paths(the_map, xc, yc, curr):
    if curr == 9:
        return [[[xc, yc]]]

    sub_paths = []
    for xd, yd in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        if the_map[xc + xd, yc + yd] == curr + 1:
            sub_paths += get_paths(the_map, xc + xd, yc + yd, curr + 1)

    return [[[xc, yc]] + sub_path for sub_path in sub_paths]


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
