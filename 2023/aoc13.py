import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 405
TEST_SOLUTION2 = 400


def solve(puzzle_input):
    patterns = []
    curr_pattern = PseudoMatrix()
    for line in puzzle_input:
        if line:
            curr_pattern.append_row(line)
        else:
            patterns.append(curr_pattern)
            curr_pattern = PseudoMatrix()
    patterns.append(curr_pattern)

    notes1 = []
    ref_lines = []
    for pattern in patterns:
        ref_line = find_ref_line(pattern)
        ref_lines.append(ref_line)
        notes1.append(get_note(ref_line))

    notes2 = []
    for i in range(0, len(patterns)):
        pattern = patterns[i]
        old_ref_line = ref_lines[i]

        ref_line = None
        for x, y in pattern.iter():
            pattern_copy = pattern.copy()
            pattern_copy[x, y] = "." if pattern[x, y] == "#" else "#"
            ref_line = find_ref_line(pattern_copy, old_ref_line)
            if ref_line and ref_line != old_ref_line:
                break

        notes2.append(get_note(ref_line))

    return sum(notes1), sum(notes2)


def find_ref_line(pattern, old_ref_line=None):
    ref_line_after_col = 0
    while ref_line_after_col < pattern.x_range[1]:
        if is_col_symmetric(pattern, ref_line_after_col):
            candidate = [ref_line_after_col, None]
            if candidate != old_ref_line:
                return candidate
            else:
                ref_line_after_col += 1
        else:
            ref_line_after_col += 1

    ref_line_after_row = 0
    while ref_line_after_row < pattern.y_range[1]:
        if is_row_symmetric(pattern, ref_line_after_row):
            candidate = [None, ref_line_after_row]
            if candidate != old_ref_line:
                return candidate
            else:
                ref_line_after_row += 1
        else:
            ref_line_after_row += 1

    return None


def is_col_symmetric(pattern, ref_line_after_col):
    x1 = ref_line_after_col
    x2 = ref_line_after_col + 1
    while x1 >= pattern.x_range[0] and x2 <= pattern.x_range[1]:
        if pattern.get_column(x1) != pattern.get_column(x2):
            return False
        else:
            x1 -= 1
            x2 += 1
    return True


def is_row_symmetric(pattern, ref_line_after_row):
    y1 = ref_line_after_row
    y2 = ref_line_after_row + 1
    while y1 >= pattern.y_range[0] and y2 <= pattern.y_range[1]:
        if pattern.get_row(y1) != pattern.get_row(y2):
            return False
        else:
            y1 -= 1
            y2 += 1
    return True


def get_note(ref_line):
    if not ref_line:
        raise Exception("Whoooot?")

    if ref_line[0] is not None:
        return ref_line[0] + 1
    if ref_line[1] is not None:
        return 100 * (ref_line[1] + 1)

    raise Exception("Whoooot?")


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
