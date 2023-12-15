import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 1320
TEST_SOLUTION2 = 145


def solve(puzzle_input):
    init_sequence = puzzle_input[0].split(",")

    hashes = [get_hash(the_string) for the_string in init_sequence]

    boxes = defaultdict(lambda: [])
    for the_string in init_sequence:
        if "=" in the_string:
            label, _ = the_string.split("=")
            box = get_hash(label)
            boxes[box] = [the_string if lens.startswith(label) else lens for lens in boxes[box]]
            if the_string not in boxes[box]:
                boxes[box].append(the_string)
        else:
            label = the_string[:-1]
            box = get_hash(label)
            boxes[box] = [lens for lens in boxes[box] if not lens.startswith(label)]

    focusing_power = 0
    for box in boxes.keys():
        for i in range(len(boxes[box])):
            lens = boxes[box][i]
            _, focal_length = lens.split("=")
            focusing_power += (box + 1) * (i + 1) * int(focal_length)

    return sum(hashes), focusing_power


def get_hash(the_string):
    the_hash = 0
    for c in the_string:
        the_hash = (the_hash + ord(c)) * 17 % 256
    return the_hash


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
