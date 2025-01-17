import math
import os
import time

TEST_SOLUTION1 = 62842880
TEST_SOLUTION2 = 57600000


def solve(puzzle_input):
    ingredients = []
    for line in puzzle_input:
        ingredient = {}
        name, properties = line.split(": ")
        ingredient["name"] = name
        for property_string in properties.split(", "):
            prop, value = property_string.split(" ")
            ingredient[prop] = int(value)
        ingredients.append(ingredient)

    total_score1 = 0
    total_score2 = 0
    for distribution in iter_distributions(100, len(ingredients)):
        total_score1 = max(total_score1, get_score(ingredients, distribution))
        if check_calories(ingredients, distribution):
            total_score2 = max(total_score2, get_score(ingredients, distribution))

    return total_score1, total_score2

def iter_distributions(the_max, the_len):
    if the_max == 0:
        return [0] * the_len

    for i in range(0, the_max+1):
        if the_len == 1:
            yield [i]
        else:
            for j in iter_distributions(the_max-i, the_len-1):
                yield [i] + j

def get_score(ingredients, distribution):
    weights = [0,0,0,0]
    for i in range(0, len(ingredients)):
        weights[0] += ingredients[i]["capacity"] * distribution[i]
        weights[1] += ingredients[i]["durability"] * distribution[i]
        weights[2] += ingredients[i]["flavor"] * distribution[i]
        weights[3] += ingredients[i]["texture"] * distribution[i]
    if sum(w < 0 for w in weights) > 0:
        return 0
    else:
        return math.prod(weights)

def check_calories(ingredients, distribution):
    calories = 0
    for i in range(0, len(ingredients)):
        calories += ingredients[i]["calories"] * distribution[i]
    return calories == 500


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
