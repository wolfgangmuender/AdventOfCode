import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 4361
TEST_SOLUTION2 = 467835


def solve(puzzle_input):
    schematic = PseudoMatrix(".")
    for line in puzzle_input:
        schematic.append_row(line)

    part_numbers = []
    curr_num = None
    is_part = False
    for x, y in schematic.iter():
        curr = schematic[x, y]
        if curr.isdigit():
            if curr_num:
                curr_num += curr
            else:
                curr_num = curr
                is_part = schematic[x - 1, y] != "."
            if not is_part:
                is_part = check_is_part(schematic, x, y)
        else:
            if curr_num and is_part:
                part_numbers.append(int(curr_num))
            curr_num = None
            is_part = False

    gears = []
    for x, y in schematic.iter():
        if schematic[x, y] == "*":
            gear = check_gear(schematic, x, y)
            if gear:
                gears.append(gear)

    return sum(part_numbers), sum([g[0] * g[1] for g in gears])


def check_is_part(schematic, x, y):
    for dx, dy in [(-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)]:
        adj = schematic[x + dx, y + dy]
        if adj != "." and not adj.isdigit():
            return True
    return False


def check_gear(schematic, x, y):
    d = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    first_num = None
    pos = 0
    for dx, dy in d:
        curr = schematic[x + dx, y + dy]
        if curr.isdigit():
            first_num = int(collect(schematic, x + dx, y + dy, -1) + curr + collect(schematic, x + dx, y + dy, 1))
            break
        pos += 1
    if not first_num:
        return None

    if pos == 0:
        if schematic[x, y - 1].isdigit():
            start = 3
        else:
            start = 2
    elif pos == 1 or pos == 2:
        start = 3
    elif pos == 3 or pos == 4:
        start = pos + 1
    elif pos == 5 and not schematic[x, y + 1].isdigit():
        start = 7
    else:
        return None

    second_num = None
    for dx, dy in d[start:]:
        curr = schematic[x + dx, y + dy]
        if curr.isdigit():
            second_num = int(collect(schematic, x + dx, y + dy, -1) + curr + collect(schematic, x + dx, y + dy, 1))
            break
    if not second_num:
        return None

    return [first_num, second_num]


def collect(schematic, x, y, d):
    num = ""
    curr = x + d
    while schematic[curr, y].isdigit():
        if d < 0:
            num = schematic[curr, y] + num
        else:
            num = num + schematic[curr, y]
        curr = curr + d
    return num


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
