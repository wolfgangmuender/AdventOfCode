import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 21
TEST_SOLUTION2 = 40


def solve(puzzle_input):
    manifold = PseudoMatrix(".")
    for line in puzzle_input:
        manifold.append_row(line)

    start = manifold.get_first_coordinate("S")
    beam_positions = {start[0]}
    num_splits = 0
    for y in range(1, manifold.get_height()):
        next_beam_positions = set()
        for beam_position in beam_positions:
            if manifold[beam_position, y] == ".":
                next_beam_positions.add(beam_position)
            elif manifold[beam_position, y] == "^":
                next_beam_positions.add(beam_position + 1)
                next_beam_positions.add(beam_position - 1)
                num_splits += 1
        beam_positions = next_beam_positions

    return num_splits, get_num_paths(manifold, {}, start[0], start[1])


def get_num_paths(manifold, cache, x, y):
    cache_key = f"{x}_{y}"
    if cache_key in cache:
        return cache[cache_key]

    if y == manifold.get_height() - 1:
        num_paths = 1
    elif manifold[x, y + 1] == ".":
        num_paths = get_num_paths(manifold, cache, x, y + 1)
    elif manifold[x, y + 1] == "^":
        num_paths = get_num_paths(manifold, cache, x - 1, y + 1) + get_num_paths(manifold, cache, x + 1, y + 1)
    else:
        raise Exception("Whoot?")

    cache[cache_key] = num_paths
    return num_paths


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
