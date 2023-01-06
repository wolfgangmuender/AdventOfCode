import os
import time

TEST_SOLUTION1 = 0
TEST_SOLUTION2 = 0


def solve(puzzle_input):
    passphrases = []
    for line in puzzle_input:
        passphrases.append(line.split(" "))

    valid_passphrases = [passphrase for passphrase in passphrases if len(passphrase) == len(set(passphrase))]
    solution1 = len(valid_passphrases)

    valid_passphrases = []
    for passphrase in passphrases:
        is_valid = True

        for i in range(0, len(passphrase)):
            for j in range(i+1, len(passphrase)):
                if sorted(passphrase[i]) == sorted(passphrase[j]):
                    is_valid = False

        if is_valid:
            valid_passphrases.append(passphrase)
    solution2 = len(valid_passphrases)

    return solution1, solution2


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
