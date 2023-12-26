import os
import time

TEST_SOLUTION1 = 2
TEST_SOLUTION2 = 0


def solve(puzzle_input):
    hailstones = []
    for line in puzzle_input:
        position, velocity = line.split(" @ ")
        hailstones.append([[int(p) for p in position.split(", ")], [int(v) for v in velocity.split(", ")]])

    if len(hailstones) == 5:
        limits = [7, 27]
    else:
        limits = [200000000000000, 400000000000000]

    num_intersections = 0
    for i in range(0, len(hailstones)):
        p1 = hailstones[i][0]
        v1 = hailstones[i][1]
        for j in range(i + 1, len(hailstones)):
            p2 = hailstones[j][0]
            v2 = hailstones[j][1]

            if v2[1] / v2[0] - v1[1] / v1[0] == 0:
                continue

            x = (p1[1] - p2[1] - v1[1] / v1[0] * p1[0] + v2[1] / v2[0] * p2[0]) / (v2[1] / v2[0] - v1[1] / v1[0])
            y = p1[1] + v1[1] / v1[0] * (x - p1[0])

            if (x - p1[0]) / v1[0] < 0 or (x - p2[0]) / v2[0] < 0:
                continue

            if limits[0] <= x <= limits[1] and limits[0] <= y <= limits[1]:
                num_intersections += 1

    return num_intersections, 0


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
