import os
import time

TEST_SOLUTION1 = 12
TEST_SOLUTION2 = 19


def solve(puzzle_input):
    code_length = 0
    memory_length = 0
    encoded_length = 0
    for line in puzzle_input:
        temp = list(line[1:-1])
        count = 0
        while temp:
            curr = temp.pop(0)
            if curr == "\\":
                if temp:
                    if temp[0] in ["\\", "\""]:
                        temp.pop(0)
                    elif temp[0] == "x":
                        temp.pop(0)
                        temp.pop(0)
                        temp.pop(0)
                    else:
                        raise Exception("Whoot?")
                else:
                    raise Exception("Whoot?")
            count += 1

        encoded = line.replace("\\", "\\\\").replace("\"", "\\\"")

        code_length += len(line)
        memory_length += count
        encoded_length += len(encoded) + 2

    return code_length - memory_length, encoded_length - code_length


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
