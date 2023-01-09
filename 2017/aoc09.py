import os
import time

TEST_SOLUTION1 = 9
TEST_SOLUTION2 = 8


def solve(puzzle_input):
    stream = list(puzzle_input[0])

    total_score = 0
    total_garbage = 0

    group_level = 0
    is_garbage = False
    while stream:
        c = stream.pop(0)
        if is_garbage:
            if c == ">":
                is_garbage = False
            elif c == "!":
                stream.pop(0)
            else:
                total_garbage += 1
        else:
            if c == "{":
                group_level += 1
            elif c == "}":
                total_score += group_level
                group_level -= 1
            elif c == "<":
                is_garbage = True

    return total_score, total_garbage


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    if os.path.isfile(test_input_file):
        with open(test_input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
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
