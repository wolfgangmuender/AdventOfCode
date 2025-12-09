import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 50
TEST_SOLUTION2 = 24


def solve(puzzle_input):
    positions = []
    for line in puzzle_input:
        positions.append([int(n) for n in line.split(",")])

    verticals = get_verticals(positions)
    horizontals = get_horizontals(positions)

    largest_square1 = 0
    largest_square2 = 0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            dx = abs(positions[i][0] - positions[j][0])
            dy = abs(positions[i][1] - positions[j][1])
            area = (dx + 1) * (dy + 1)
            largest_square1 = max(area, largest_square1)
            if is_only_red_and_green(positions[i][0], positions[i][1], positions[j][0], positions[j][1], verticals, horizontals):
                largest_square2 = max(area, largest_square2)

    return largest_square1, largest_square2


def is_only_red_and_green(x1, y1, x2, y2, verticals, horizontals):
    if x1 == x2 or y1 == y2:
        # it's very unlikely that a single line has the largest area and I don't want to deal with it
        return False

    xvs = sorted(verticals.keys())
    yhs = sorted(horizontals.keys())

    xa = (x1 + 0.5) if x1 < x2 else (x2 + 0.5)
    xb = (x2 - 0.5) if x1 < x2 else (x1 - 0.5)
    ya = (y1 + 0.5) if y1 < y2 else (y2 + 0.5)
    yb = (y2 - 0.5) if y1 < y2 else (y1 - 0.5)

    is_inside = []
    for xv in xvs:
        if xv < xa:
            for vert in verticals[xv]:
                if vert[0] < ya < vert[1]:
                    is_inside = not is_inside
                    break
        elif not is_inside:
            return False
        elif xv < xb:
            for vert in verticals[xv]:
                if intersects(ya, yb, vert[0], vert[1]):
                    return False
        else:
            break

    for yh in yhs:
        if ya < yh < yb:
            for horiz in horizontals[yh]:
                if intersects(xa, xb, horiz[0], horiz[1]):
                    return False

    return True


def intersects(a_start, a_end, b_start, b_end):
    return max(a_start, b_start) < min(a_end, b_end)


def get_verticals(positions):
    verticals = defaultdict(list)
    for i in range(len(positions)):
        ind1 = i
        ind2 = 0 if i == len(positions) - 1 else i + 1
        if positions[ind1][0] == positions[ind2][0]:
            vert = [positions[ind1][1], positions[ind2][1]] if positions[ind1][1] < positions[ind2][1] else [positions[ind2][1], positions[ind1][1]]
            verticals[positions[ind1][0]].append(vert)
    return verticals


def get_horizontals(positions):
    horizontals = defaultdict(list)
    for i in range(len(positions)):
        ind1 = i
        ind2 = 0 if i == len(positions) - 1 else i + 1
        if positions[ind1][1] == positions[ind2][1]:
            horiz = [positions[ind1][0], positions[ind2][0]] if positions[ind1][0] < positions[ind2][0] else [positions[ind2][0], positions[ind1][0]]
            horizontals[positions[ind1][1]].append(horiz)
    return horizontals


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
