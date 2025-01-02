import os
import re
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 998996
TEST_SOLUTION2 = 1001996

REG = re.compile("^(turn on|turn off|toggle) ([0-9]+),([0-9]+) through ([0-9]+),([0-9]+)$")


def solve(puzzle_input):
    commands = []
    for line in puzzle_input:
        res = REG.match(line)
        commands.append([res.group(1), int(res.group(2)), int(res.group(3)), int(res.group(4)), int(res.group(5))])

    lights1 = PseudoMatrix(".")
    lights2 = PseudoMatrix(0)
    total_brightness = 0
    for command in commands:
        op, x1, y1, x2, y2 = command
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if op == "turn on":
                    lights1[x, y] = "#"
                    lights2[x, y] += 1
                    total_brightness += 1
                elif op == "turn off":
                    lights1[x, y] = "."
                    diff = -1 if lights2[x, y] > 0 else 0
                    lights2[x, y] += diff
                    total_brightness += diff
                elif op == "toggle":
                    lights1[x, y] = "#" if lights1[x, y] == "." else "."
                    lights2[x, y] += 2
                    total_brightness += 2
                else:
                    raise Exception("Whoot?")

    return lights1.count("#"), total_brightness


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
