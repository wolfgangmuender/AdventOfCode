import os
import time

TEST_SOLUTION1 = 3
TEST_SOLUTION2 = 14


def solve(puzzle_input):
    ranges = []
    ingredients = []
    for line in puzzle_input:
        if not line:
            continue
        elif "-" in line:
            ranges.append(list(map(int, line.split("-"))))
        else:
            ingredients.append(int(line))

    # sort ranges by first element
    ranges.sort(key=lambda x: x[0])
    print(ranges)

    num_fresh =  0
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                num_fresh += 1
                break

    num_fresh2 =  0
    curr_max = 0
    for r in ranges:
        if r[1] <= curr_max:
            pass
        elif r[0] <= curr_max:
            num_fresh2 += r[1] - curr_max
        else:
            num_fresh2 += r[1] - r[0] + 1
        curr_max = max(curr_max, r[1])

    return num_fresh, num_fresh2


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
