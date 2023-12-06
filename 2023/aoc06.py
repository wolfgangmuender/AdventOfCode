import os
import time
from functools import reduce

TEST_SOLUTION1 = 288
TEST_SOLUTION2 = 71503


def solve(puzzle_input):
    times = []
    distances = []
    real_time = None
    real_distance = None
    for line in puzzle_input:
        if line.startswith("Time:"):
            times = [int(n.strip()) for n in line.replace("Time:", "").split(" ") if n.strip()]
            real_time = int(line.replace("Time:", "").replace(" ", ""))
        elif line.startswith("Distance:"):
            distances = [int(n.strip()) for n in line.replace("Distance:", "").split(" ") if n.strip()]
            real_distance = int(line.replace("Distance:", "").replace(" ", ""))
        else:
            raise Exception("Whoot?")

    results = []
    wins = []
    for i in range(0, len(times)):
        the_time = times[i]
        the_result = [(the_time - curr_time) * curr_time for curr_time in range(0, the_time + 1)]
        results.append(the_result)
        wins.append([r for r in the_result if r > distances[i]])

    real_result = []
    for curr_time in range(0, real_time + 1):
        real_result.append((real_time - curr_time) * curr_time)

    return (reduce(lambda x, y: x * y, [len(w) for w in wins]),
            sum([1 for i in range(0, len(real_result)) if real_result[i] > real_distance]))


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
