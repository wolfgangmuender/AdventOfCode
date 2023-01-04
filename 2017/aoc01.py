import os
import time

TEST_SOLUTION1 = 0
TEST_SOLUTION2 = 12


def solve(puzzle_input):
    captcha = [int(c) for c in puzzle_input[0]]

    return count(captcha, 1), count(captcha, int(len(captcha)/2))


def count(captcha, offset):
    res = 0
    for i in range(0, len(captcha)):
        if i + offset >= len(captcha):
            if captcha[i] == captcha[i + offset - len(captcha)]:
                res += captcha[i]
        elif captcha[i] == captcha[i+offset]:
            res += captcha[i]
    return res


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    if os.path.isfile(test_input_file):
        with open(test_input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
        if solution1 != TEST_SOLUTION1:
            print(f"Solution 1 '{solution1}' not correct for test input")
            return
        if solution2 != TEST_SOLUTION2:
            print(f"Solution 2 '{solution2}' not correct for test input")
            return
        end = time.time()
        print_diff(end - start)
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
        print_diff(end - start)
    else:
        open(input_file, 'a').close()


def print_diff(diff):
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))


if __name__ == "__main__":
    main()
