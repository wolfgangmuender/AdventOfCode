import os
import time

TEST_SOLUTION1 = 605
TEST_SOLUTION2 = 982


def solve(puzzle_input):
    cities = set()
    distances = {}
    for line in puzzle_input:
        cities_string, distance = line.split(" = ")
        city1, city2 = cities_string.split(" to ")
        cities.add(city1)
        cities.add(city2)
        distances[key(city1,city2)] = int(distance)

    return get_extreme_distances(None, cities, distances)

def get_extreme_distances(the_city, cities, distances):
    if not cities:
        return 0, 0

    total_max_distance = None
    total_min_distance = None
    for city in cities:
        distance1 = distances[key(the_city,city)] if the_city else 0
        sub_min_distance, sub_max_distance = get_extreme_distances(city, get_others(city, cities), distances)
        min_distance = distance1 + sub_min_distance
        max_distance = distance1 + sub_max_distance

        total_min_distance = min_distance if not total_min_distance or min_distance < total_min_distance else total_min_distance
        total_max_distance = max_distance if not total_max_distance or max_distance > total_max_distance else total_max_distance

    return total_min_distance, total_max_distance


def get_others(the_city, cities):
    return [city for city in cities if city != the_city]


def key(city1,city2):
    return tuple(sorted([city1,city2]))


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
