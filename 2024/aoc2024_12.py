import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 1930
TEST_SOLUTION2 = 1206


def solve(puzzle_input):
    garden_map = PseudoMatrix(".")
    for line in puzzle_input:
        garden_map.append_row([c for c in line])

    total_price1 = 0
    total_price2 = 0
    visited = set()
    for x, y in garden_map.iter():
        if tuple([x, y]) in visited:
            continue

        region, region_perimeter = explore_region(garden_map, x, y)
        visited.update([tuple(r) for r in region])

        total_price1 += len(region) * len(region_perimeter)
        total_price2 += len(region) * count_sides(region_perimeter)

    return total_price1, total_price2


def explore_region(garden_map, xs, ys):
    region_id = garden_map[xs, ys]
    region = set()
    region_perimeter = []

    to_visit = {tuple([xs, ys])}
    while to_visit:
        curr = to_visit.pop()
        x, y = curr

        region.add(curr)
        for xd, yd in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            if garden_map[x + xd, y + yd] == region_id:
                if tuple([x + xd, y + yd]) not in region and tuple([x + xd, y + yd]) not in to_visit:
                    to_visit.add(tuple([x + xd, y + yd]))
            else:
                region_perimeter.append([x, y, xd, yd])

    return region, region_perimeter


def count_sides(region_perimeter):
    points = []
    directions = []
    for entry in region_perimeter:
        x, y, xd, yd = entry
        if xd == 0 and yd == 1:
            xs = 10 * x + 5
            ys = 10 * y + 5
            points.append(tuple([xs, ys]))
            directions.append([-10, 0])
        elif xd == 0 and yd == -1:
            xs = 10 * x - 5
            ys = 10 * y - 5
            points.append(tuple([xs, ys]))
            directions.append([10, 0])
        elif xd == 1 and yd == 0:
            xs = 10 * x + 5
            ys = 10 * y - 5
            points.append(tuple([xs, ys]))
            directions.append([0, 10])
        elif xd == -1 and yd == 0:
            xs = 10 * x - 5
            ys = 10 * y + 5
            points.append(tuple([xs, ys]))
            directions.append([0, -10])
        else:
            raise Exception("Whoot?")

    total_num_sides = 0
    while points:
        num_sides = 1

        start_point = points.pop()
        start_direction = directions.pop()
        curr_point = start_point
        curr_direction = start_direction
        next_point, next_direction = get_next_point(curr_point, curr_direction, points, directions)
        while next_point:
            i = points.index(next_point)
            del points[i]
            del directions[i]
            if curr_direction != next_direction:
                num_sides += 1
            curr_point = next_point
            curr_direction = next_direction
            next_point, next_direction = get_next_point(curr_point, curr_direction, points, directions)
        if curr_direction == start_direction:
            num_sides -= 1

        total_num_sides += num_sides

    return total_num_sides


def get_next_point(curr_point, curr_direction, points, directions):
    x, y = curr_point
    xd, yd = curr_direction
    next_point = tuple([x + xd, y + yd])
    if next_point in points:
        return next_point, directions[points.index(next_point)]
    else:
        return None, None


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
