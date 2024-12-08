import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 14
TEST_SOLUTION2 = 34


def solve(puzzle_input):
    all_antennas = defaultdict(lambda: list())
    x = 0
    y = 0
    for line in puzzle_input:
        x = 0
        for c in line:
            if c != ".":
                all_antennas[c].append([x, y])
            x += 1
        y += 1
    xm = x - 1
    ym = y - 1

    unique_antinodes1 = set()
    for frequency, antennas in all_antennas.items():
        for i in range(0, len(antennas)):
            for j in range(i + 1, len(antennas)):
                unique_antinodes1.update(get_antinodes1(xm, ym, antennas[i], antennas[j]))

    unique_antinodes2 = set()
    for frequency, antennas in all_antennas.items():
        for i in range(0, len(antennas)):
            for j in range(i + 1, len(antennas)):
                unique_antinodes2.update(get_antinodes2(xm, ym, antennas[i], antennas[j]))

    return len(unique_antinodes1), len(unique_antinodes2)


def get_antinodes1(xm, ym, antenna1, antenna2):
    antinodes = []
    xd = antenna2[0] - antenna1[0]
    yd = antenna2[1] - antenna1[1]

    x1 = antenna2[0] + xd
    y1 = antenna2[1] + yd
    if 0 <= x1 <= xm and 0 <= y1 <= ym:
        antinodes.append([x1, y1])

    x2 = antenna1[0] - xd
    y2 = antenna1[1] - yd
    if 0 <= x2 <= xm and 0 <= y2 <= ym:
        antinodes.append([x2, y2])

    return [tuple(antinode) for antinode in antinodes]


def get_antinodes2(xm, ym, antenna1, antenna2):
    antinodes = [antenna1, antenna2]
    xd = antenna2[0] - antenna1[0]
    yd = antenna2[1] - antenna1[1]

    x = antenna2[0]
    y = antenna2[1]
    while 0 <= x + xd <= xm and 0 <= y + yd <= ym:
        x += xd
        y += yd
        antinodes.append([x, y])

    x = antenna1[0]
    y = antenna1[1]
    while 0 <= x - xd <= xm and 0 <= y - yd <= ym:
        x -= xd
        y -= yd
        antinodes.append([x, y])

    return [tuple(antinode) for antinode in antinodes]


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
