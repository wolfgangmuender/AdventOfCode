import os
import time

TEST_SOLUTION1 = 1227775554
TEST_SOLUTION2 = 4174379265


def solve(puzzle_input):
    id_ranges = [list(map(int, entry.split("-"))) for entry in puzzle_input[0].split(",")]

    sum_invalid = 0
    sum_invalid2 = 0
    for id_range in id_ranges:
        for n in range(id_range[0], id_range[1] + 1):
            if is_invalid(n):
                sum_invalid += n
            if is_invalid2(n):
                sum_invalid2 += n

    return sum_invalid, sum_invalid2


def is_invalid(id_num):
    id_str = str(id_num)
    id_len = len(id_str)
    id_len2 = int(len(id_str) / 2)
    return id_len % 2 == 0 and id_str[0:id_len2] == id_str[-id_len2:]


def is_invalid2(id_num):
    print(id_num)
    id_str = str(id_num)
    id_len2 = int(len(id_str) / 2)
    for i in range(1, id_len2 + 1):
        chunks = [id_str[j:j + i] for j in range(0, len(id_str), i)]
        if len(chunks) >= 2 and all(chunk == chunks[0] for chunk in chunks):
            return True
    return False


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
