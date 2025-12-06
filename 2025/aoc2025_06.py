import os
import time

TEST_SOLUTION1 = 4277556
TEST_SOLUTION2 = 3263827


def solve(puzzle_input):
    numbers = []
    symbols = []
    for line in puzzle_input:
        if line.startswith("*") or line.startswith("+"):
            symbols = [s for s in line.split(" ") if s]
        else:
            numbers.append([int(n) for n in line.split(" ") if n])

    grand_total = 0
    for i in range(len(symbols)):
        symbol = symbols[i]
        if symbol == "*":
            product = 1
            for number_list in numbers:
                product *= number_list[i]
            grand_total += product
        elif symbol == "+":
            summation = 0
            for number_list in numbers:
                summation += number_list[i]
            grand_total += summation

    n = len(puzzle_input)
    grand_total2 = 0
    skip = False
    curr = []
    for i in range(len(puzzle_input[0])):
        ind = len(puzzle_input[0]) - i - 1
        if skip:
            skip = False
            curr = []
            continue
        else:
            curr.append(int("".join([puzzle_input[j][ind] for j in range(n - 1)])))
            if puzzle_input[n-1][ind] == "*":
                product = 1
                for num in curr:
                    product *= num
                grand_total2 += product
                skip = True
            elif puzzle_input[n-1][ind] == "+":
                summation = 0
                for num in curr:
                    summation += num
                grand_total2 += summation
                skip = True

    return grand_total, grand_total2


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
