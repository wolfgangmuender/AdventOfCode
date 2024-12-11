import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 12
TEST_SOLUTION2 = 12


def solve(puzzle_input):
    rules = []
    for line in puzzle_input:
        patterns = [map_to_pseudo_matrix(pattern_string) for pattern_string in line.split(" => ")]
        rules.append({
            "source": mutate_pattern(patterns[0]),
            "target": patterns[1]
        })

    result1 = evolve(rules, 2 if len(rules) == 2 else 5)
    result2 = evolve(rules, 2 if len(rules) == 2 else 18)

    return get_num_pixels(result1), get_num_pixels(result2)


def map_to_pseudo_matrix(pattern_string):
    pattern = PseudoMatrix()
    x = 0
    y = 0
    for c in pattern_string:
        if c == "/":
            x = 0
            y += 1
        else:
            pattern[x, y] = c
            x += 1
    return pattern


def mutate_pattern(pattern):
    rotate1 = pattern.rotate_right()
    rotate2 = rotate1.rotate_right()
    rotate3 = rotate2.rotate_right()
    return [pattern, pattern.flip_horizontally(), pattern.flip_vertically(), rotate1, rotate1.flip_horizontally(), rotate1.flip_vertically(), rotate2, rotate2.flip_horizontally(),
            rotate2.flip_vertically(), rotate3, rotate3.flip_horizontally(), rotate3.flip_vertically()]


def evolve(rules, num_iterations):
    curr = PseudoMatrix()
    curr.append_row([".", "#", "."])
    curr.append_row([".", ".", "#"])
    curr.append_row(["#", "#", "#"])

    for i in range(0, num_iterations):
        sub_length = 2 if curr.get_width() % 2 == 0 else 3
        sub_num = curr.get_width() // sub_length

        subs = []
        for n in range(0, sub_num):
            for m in range(0, sub_num):
                subs.append(curr.get_sub(m * sub_length, (m + 1) * sub_length - 1, n * sub_length, (n + 1) * sub_length - 1))

        subs = [enhance(sub, rules) for sub in subs]
        sub_length += 1

        curr = PseudoMatrix()
        for n in range(0, sub_num):
            for m in range(0, sub_num):
                sub = subs.pop(0)
                for x, y in sub.iter():
                    curr[m * sub_length + x, n * sub_length + y] = sub[x, y]

    return curr


def enhance(pattern, rules):
    for rule in rules:
        if pattern in rule["source"]:
            return rule["target"]
    raise Exception("Whoot?")


def get_num_pixels(pattern):
    num_pixels = 0
    for x, y in pattern.iter():
        if pattern[x, y] == "#":
            num_pixels += 1
    return num_pixels


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
