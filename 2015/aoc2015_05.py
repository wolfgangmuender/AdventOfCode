import os
import time

TEST_SOLUTION1 = 2
TEST_SOLUTION2 = 2


def solve(puzzle_input):
    num_nice1 = 0
    num_nice2 = 0
    for line in puzzle_input:
        num_vowels = 0
        has_double = False
        has_pair_twice = False
        has_letter_twice = False
        for i in range(0, len(line)):
            if line[i] in ["a", "e", "i", "o", "u"]:
                num_vowels += 1
            if i < len(line) - 1 and line[i] == line[i + 1]:
                has_double = True
            if i < len(line) - 3:
                pair = line[i:i+2]
                if line.find(pair, i+2) > -1:
                    has_pair_twice = True
            if i < len(line) - 2 and line[i] == line[i+2]:
                has_letter_twice = True
        has_forbidden_string = "ab" in line or "cd" in line or "pq" in line or "xy" in line

        if num_vowels >= 3 and has_double and not has_forbidden_string:
            num_nice1 += 1
        if has_pair_twice and has_letter_twice:
            num_nice2 += 1

    return num_nice1, num_nice2


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
