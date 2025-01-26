import os
import time

TEST_SOLUTION1 = 2
TEST_SOLUTION2 = 2


def solve(puzzle_input):
    instructions = puzzle_input

    return execute({"a": 0, "b": 0}, instructions), execute({"a": 1, "b": 0}, instructions)


def execute(regs, instructions):
    i = 0
    while 0 <= i < len(instructions):
        curr = instructions[i]
        if curr.startswith("hlf"):
            regs[curr[4:]] = int(regs[curr[4:]] / 2)
            i += 1
        elif curr.startswith("tpl"):
            regs[curr[4:]] *= 3
            i += 1
        elif curr.startswith("inc"):
            regs[curr[4:]] += 1
            i += 1
        elif curr.startswith("jmp"):
            i += int(curr[4:])
        elif curr.startswith("jie"):
            r, offset = curr[4:].split(", ")
            if regs[r] % 2 == 0:
                i += int(offset)
            else:
                i += 1
        elif curr.startswith("jio"):
            r, offset = curr[4:].split(", ")
            if regs[r] == 1:
                i += int(offset)
            else:
                i += 1
        else:
            raise Exception("Whoot?")

    return regs["b"]


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
