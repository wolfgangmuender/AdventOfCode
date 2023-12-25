import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 94
TEST_SOLUTION2 = 154


def solve(puzzle_input):
    hiking_map = PseudoMatrix()
    for line in puzzle_input:
        hiking_map.append_row(line)

    start_point = get_start_point(hiking_map)

    return max(traverse(hiking_map, start_point, True)), max(traverse(hiking_map, start_point, False))


def traverse(hiking_map, start_point, is_slippery):
    num_steps = []
    paths = [[start_point]]
    while paths:
        path = paths.pop()
        next_points = get_next_points(hiking_map, path) if is_slippery else get_next_points2(hiking_map, path)
        while next_points:
            if len(next_points) > 1:
                for next_point in next_points:
                    paths.append(path + [next_point])
                break
            else:
                path += next_points
            next_points = get_next_points(hiking_map, path) if is_slippery else get_next_points2(hiking_map, path)
        if path[-1][1] == hiking_map.y_range[1]:
            num_steps.append(len(path) - 1)
    return num_steps

def get_start_point(hiking_map):
    for x in hiking_map.iter_x():
        if hiking_map[x, 0] == ".":
            return [x, 0]
    raise Exception("Whoot?")


def get_next_points(hiking_map, path):
    x, y = path[-1]
    if y == hiking_map.y_range[1]:
        return []
    elif hiking_map[x, y] == "^":
        return [[x, y - 1]]
    elif hiking_map[x, y] == ">":
        return [[x + 1, y]]
    elif hiking_map[x, y] == "v":
        return [[x, y + 1]]
    elif hiking_map[x, y] == "<":
        return [[x - 1, y]]
    else:
        next_points = []
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            xn = x + d[0]
            yn = y + d[1]
            if yn > 0 and [xn, yn] not in path:
                if d[0] == 1 and hiking_map[xn, yn] in [".", ">"]:
                    next_points.append([xn, yn])
                if d[0] == -1 and hiking_map[xn, yn] in [".", "<"]:
                    next_points.append([xn, yn])
                if d[1] == 1 and hiking_map[xn, yn] in [".", "v"]:
                    next_points.append([xn, yn])
                if d[1] == -1 and hiking_map[xn, yn] in [".", "^"]:
                    next_points.append([xn, yn])
        return next_points


def get_next_points2(hiking_map, path):
    x, y = path[-1]
    if y == hiking_map.y_range[1]:
        return []
    else:
        next_points = []
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            xn = x + d[0]
            yn = y + d[1]
            if yn > 0 and [xn, yn] not in path and hiking_map[xn, yn] != "#":
                next_points.append([xn, yn])
        return next_points


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
