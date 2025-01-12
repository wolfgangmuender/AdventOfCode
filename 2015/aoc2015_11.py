import os
import time

TEST_SOLUTION1 = "ghjaabcc"
TEST_SOLUTION2 = "ghjbbcdd"

ALPHABET_MAP = {chr(i): i - ord('a') for i in range(ord('a'), ord('z') + 1)}
NUMBER_MAP = {v: k for k, v in ALPHABET_MAP.items()}


def solve(puzzle_input):
    initial_password = puzzle_input[0]

    curr = to_numbers(initial_password)
    while not is_correct(curr):
        increment(curr, 7)
    password1 = to_string(curr)

    increment(curr, 7)
    while not is_correct(curr):
        increment(curr, 7)
    password2 = to_string(curr)

    return password1, password2


def to_numbers(password):
    return [ALPHABET_MAP[c] for c in password]


def to_string(numbers):
    return "".join([NUMBER_MAP[n] for n in numbers])


def is_correct(password):
    three_straight = False
    num_pairs = 0
    check_for_pair = True
    for i in range(0, len(password)):
        if password[i] in [8, 11, 14]:
            return False
        if i < len(password) - 1 and check_for_pair:
            if password[i] == password[i + 1]:
                num_pairs += 1
                check_for_pair = False
        else:
            check_for_pair = True
        if i < len(password) - 2:
            if password[i] + 1 == password[i + 1] and password[i] + 2 == password[i + 2]:
                three_straight = True
    return three_straight and num_pairs >= 2


def increment(password, i):
    if password[i] == 25:
        password[i] = 0
        increment(password, i - 1)
    elif password[i] in [7, 10, 13]:
        password[i] += 2
    else:
        password[i] += 1


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
