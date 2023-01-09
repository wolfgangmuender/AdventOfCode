import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 1
TEST_SOLUTION2 = 10


def solve(puzzle_input):
    instructions = []
    for line in puzzle_input:
        action, condition = line.split(" if ")
        register, cmd, value = action.split(" ")
        condition_register, comparator, reference = condition.split(" ")

        instructions.append({
            "register": register,
            "diff": int(value) if cmd == "inc" else -int(value),
            "condition_register": condition_register,
            "condition_check": f"{comparator} {reference}",
        })

    registers = defaultdict(lambda: 0)
    highest_value_ever = 0
    for instruction in instructions:
        condition_result = eval(f"{registers[instruction['condition_register']]} {instruction['condition_check']}")
        if condition_result:
            registers[instruction["register"]] += instruction["diff"]
            highest_value_ever = max(highest_value_ever, registers[instruction["register"]])

    return max(registers.values()), highest_value_ever


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
