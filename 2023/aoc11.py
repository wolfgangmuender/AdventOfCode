import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 374
TEST_SOLUTION2 = 82000210


def solve(puzzle_input):
    image = PseudoMatrix(".")
    for line in puzzle_input:
        image.append_row(line)

    expanded_image, empty_cols = expand_columns(image)
    expanded_image, empty_rows = expand_rows(expanded_image)

    distances1 = get_distances1(expanded_image)
    distances1_check = get_distances2(image, empty_cols, empty_rows, 2)
    distances2 = get_distances2(image, empty_cols, empty_rows, 1000000)

    assert distances1 == distances1_check

    return sum(distances1), sum(distances2)


def expand_columns(image):
    expanded_image = PseudoMatrix(".")
    empty_columns = []
    for x, col in image.iter_columns():
        expanded_image.append_column(col)
        if all(p == "." for p in col):
            expanded_image.append_column(col)
            empty_columns.append(x)
    return expanded_image, empty_columns


def expand_rows(image):
    expanded_image = PseudoMatrix(".")
    empty_rows = []
    for y, row in image.iter_rows():
        expanded_image.append_row(row)
        if all(p == "." for p in row):
            expanded_image.append_row(row)
            empty_rows.append(y)
    return expanded_image, empty_rows


def get_distances1(expanded_image):
    galaxies = {}
    galaxy_count = 0
    for x, y in expanded_image.iter():
        if expanded_image[x, y] == "#":
            galaxies[galaxy_count] = [x, y]
            galaxy_count += 1

    distances = []
    for gn1 in galaxies.keys():
        for gn2 in galaxies.keys():
            if gn2 > gn1:
                distances.append(abs(galaxies[gn2][1] - galaxies[gn1][1]) + abs(galaxies[gn2][0] - galaxies[gn1][0]))

    return distances


def get_distances2(image, empty_cols, empty_rows, expansion_factor):
    galaxies = {}
    galaxy_count = 0
    for x, y in image.iter():
        if image[x, y] == "#":
            galaxies[galaxy_count] = [x, y]
            galaxy_count += 1

    distances = []
    for gn1 in galaxies.keys():
        for gn2 in galaxies.keys():
            if gn2 > gn1:
                x1 = galaxies[gn1][0]
                x2 = galaxies[gn2][0]
                xdist = 0
                xrange = range(x1 + 1, x2 + 1) if x2 >= x1 else range(x2 + 1, x1 + 1)
                for x in xrange:
                    if x in empty_cols:
                        xdist += expansion_factor
                    else:
                        xdist += 1

                y1 = galaxies[gn1][1]
                y2 = galaxies[gn2][1]
                yrange = range(y1 + 1, y2 + 1) if y2 > y1 else range(y2 + 1, y1 + 1)
                ydist = 0
                for y in yrange:
                    if y in empty_rows:
                        ydist += expansion_factor
                    else:
                        ydist += 1

                distances.append(xdist + ydist)

    return distances


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
