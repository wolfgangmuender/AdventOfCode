import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 13
TEST_SOLUTION2 = 43


def solve(puzzle_input):
    paper_rolls = PseudoMatrix(".")
    for line in puzzle_input:
        paper_rolls.append_row(line)

    num_acessible = 0
    for x,y in paper_rolls.iter():
        if paper_rolls[x,y] == "@" and sum([1 if paper_rolls[xn,yn] == "@" else 0 for xn,yn in paper_rolls.iter_direct_neighbours(x, y, True)]) < 4:
            num_acessible += 1

    num_acessible2 = 0
    delta = None
    paper_rolls_cleared = paper_rolls.copy()
    while delta != 0:
        delta = 0
        for x,y in paper_rolls_cleared.iter():
            if paper_rolls_cleared[x,y] == "@" and sum([1 if paper_rolls_cleared[xn,yn] == "@" else 0 for xn,yn in paper_rolls_cleared.iter_direct_neighbours(x, y, True)]) < 4:
                paper_rolls_cleared[x,y] = "."
                delta += 1
        num_acessible2 += delta

    return num_acessible, num_acessible2


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
