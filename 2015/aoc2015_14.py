import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 1120
TEST_SOLUTION2 = 689


def solve(puzzle_input):
    reindeers = []
    for line in puzzle_input:
        name, remainder = line.split(" can fly ")
        speed, remainder = remainder.split(" km/s for ")
        fly_time, rest_time = remainder[:-9].split(" seconds, but then must rest for ")
        reindeers.append({
            "name": name,
            "speed": int(speed),
            "fly_time": int(fly_time),
            "rest_time": int(rest_time),
        })

    time_limit = 2503 if len(reindeers) > 2 else 1000

    points = defaultdict(lambda: 0)
    positions = defaultdict(lambda: 0)
    curr_time = 0
    while curr_time < time_limit:
        for reindeer in reindeers:
            cycle_time = reindeer["fly_time"] + reindeer["rest_time"]
            is_flying = curr_time % cycle_time < reindeer["fly_time"]
            if is_flying:
                positions[reindeer["name"]] += reindeer["speed"]

        lead = max(positions.values())
        for reindeer in reindeers:
            if positions[reindeer["name"]] == lead:
                points[reindeer["name"]] += 1

        curr_time += 1

    return max(positions.values()), max(points.values())


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
