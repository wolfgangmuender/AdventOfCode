import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 7
TEST_SOLUTION2 = 5


def solve(puzzle_input):
    input_molecule = None
    replacements = []
    for line in puzzle_input:
        if "=>" in line:
            source, target = line.split(" => ")
            replacements.append([source, target])
        elif line:
            input_molecule = line

    calibration = replace(input_molecule, replacements)

    elements = defaultdict(lambda: 0)
    i = 0
    while i < len(input_molecule):
        if i < len(input_molecule) - 1 and input_molecule[i + 1].islower():
            elements[input_molecule[i:i + 2]] += 1
            i += 2
        else:
            elements[input_molecule[i]] += 1
            i += 1

    return len(calibration), sum(elements.values()) - (elements["Rn"] + elements["Ar"]) - 2 * elements["Y"] - 1


def replace(input_molecule, replacements):
    molecules = set()
    for i in range(0, len(input_molecule)):
        for replacement in replacements:
            source, target = replacement
            if input_molecule[i] == source:
                molecules.add(input_molecule[:i] + target + input_molecule[i + 1:])
            if input_molecule[i:i + 2] == source:
                molecules.add(input_molecule[:i] + target + input_molecule[i + 2:])
    return molecules


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
