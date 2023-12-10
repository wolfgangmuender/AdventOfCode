import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 8
TEST_SOLUTION2 = 10


def solve(puzzle_input):
    the_map = PseudoMatrix(".")
    for line in puzzle_input:
        the_map.append_row(line)

    xs, ys = get_start(the_map)

    x1, y1 = xs, ys
    x2, y2 = get_first_next(the_map, x1, y1)
    pipe_fields = [[x1, y1]]
    steps = 0
    while the_map[x2, y2] != "S":
        x, y = x2, y2
        x2, y2 = get_next(the_map, x1, y1, x2, y2)
        x1, y1 = x, y
        pipe_fields.append([x1, y1])
        steps += 1

    start_form = get_start_form(the_map, xs, ys)
    the_map[xs, ys] = start_form

    inside_count = 0
    is_inside = False
    for x, y in the_map.iter():
        if [x, y] in pipe_fields:
            if the_map[x, y] in ["|", "L", "J"]:
                is_inside = not is_inside
        elif is_inside:
            inside_count += 1

    return int((steps + 1) / 2), inside_count


def get_start(the_map):
    for x, y in the_map.iter():
        if the_map[x, y] == "S":
            return x, y
    raise Exception("Whoooot?")


def get_first_next(the_map, x1, y1):
    if the_map[x1 + 1, y1] in ["-", "J", "7"]:
        return x1 + 1, y1
    elif the_map[x1 - 1, y1] in ["-", "L", "F"]:
        return x1 - 1, y1
    elif the_map[x1, y1 + 1] in ["|", "L", "J"]:
        return x1, y1 + 1
    elif the_map[x1, y1 - 1] in ["|", "7", "F"]:
        return x1, y1 - 1
    else:
        raise Exception("Whoooot?")


def get_next(the_map, x1, y1, x2, y2):
    if the_map[x2, y2] == "|":
        if y2 + 1 == y1:
            return x2, y2 - 1
        else:
            return x2, y2 + 1
    elif the_map[x2, y2] == "-":
        if x2 + 1 == x1:
            return x2 - 1, y2
        else:
            return x2 + 1, y2
    elif the_map[x2, y2] == "L":
        if y2 - 1 == y1:
            return x2 + 1, y2
        else:
            return x2, y2 - 1
    elif the_map[x2, y2] == "J":
        if y2 - 1 == y1:
            return x2 - 1, y2
        else:
            return x2, y2 - 1
    elif the_map[x2, y2] == "7":
        if y2 + 1 == y1:
            return x2 - 1, y2
        else:
            return x2, y2 + 1
    elif the_map[x2, y2] == "F":
        if y2 + 1 == y1:
            return x2 + 1, y2
        else:
            return x2, y2 + 1
    else:
        raise Exception("Whoooot?")


def get_start_form(the_map, xs, ys):
    goes_north = the_map[xs, ys - 1] in ["|", "F", "7"]
    goes_east = the_map[xs + 1, ys] in ["-", "J", "7"]
    goes_south = the_map[xs, ys + 1] in ["|", "L", "J"]
    goes_west = the_map[xs - 1, ys] in ["-", "L", "F"]
    if goes_north and goes_east:
        return "L"
    elif goes_north and goes_south:
        return "|"
    elif goes_north and goes_west:
        return "J"
    elif goes_south and goes_east:
        return "F"
    elif goes_south and goes_west:
        return "7"
    elif goes_east and goes_west:
        return "-"
    else:
        raise Exception("Whoooot?")


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
