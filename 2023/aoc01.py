import os
import time

TEST_SOLUTION1 = 142
TEST_SOLUTION2 = 281

NUMBERS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
}


def solve(puzzle_input):
    digits1 = []
    digits2 = []

    for line in puzzle_input:
        res1 = {}
        res2 = {}

        i = 0
        for c in line:
            if c.isdigit():
                res1[i] = c
                res2[i] = c
            i += 1

        for number in NUMBERS.keys():
            i = line.find(number)
            if i >= 0:
                res2[i] = NUMBERS[number]
            i = line.rfind(number)
            if i >= 0:
                res2[i] = NUMBERS[number]

        if res1:
            digits1.append(int(res1[min(res1.keys())] + res1[max(res1.keys())]))
        digits2.append(int(res2[min(res2.keys())] + res2[max(res2.keys())]))

    return sum(digits1), sum(digits2)


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
