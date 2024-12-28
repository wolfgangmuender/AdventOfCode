import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 3
TEST_SOLUTION2 = 0


def solve(puzzle_input):
    schematics = []
    schematic = PseudoMatrix()
    for line in puzzle_input:
        if not line:
            schematics.append(schematic)
            schematic = PseudoMatrix()
        else:
            schematic.append_row(line)
    schematics.append(schematic)

    locks = []
    keys = []
    for schematic in schematics:
        num = []
        for _, column in schematic.iter_columns():
            num.append(column.count("#") - 1)
        if schematic[0, 0] == "#":
            locks.append(num)
        elif schematic[0, 0] == ".":
            keys.append(num)
        else:
            raise Exception("Whoot?")

    num_fits = 0
    for lock in locks:
        for key in keys:
            if fits(lock, key):
                num_fits += 1

    return num_fits, 0


def fits(lock, key):
    for i in range(0, len(lock)):
        if lock[i] + key[i] > 5:
            return False
    return True


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
