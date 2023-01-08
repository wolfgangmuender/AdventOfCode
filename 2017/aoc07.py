import os
import time

TEST_SOLUTION1 = "tknk"
TEST_SOLUTION2 = 60


def solve(puzzle_input):
    towers = {}
    for line in puzzle_input:
        if " -> " in line:
            tower_spec, sub_towers = line.split(" -> ")
        else:
            tower_spec, sub_towers = line, ""
        tower_name, tower_weight = tower_spec.split(" ")
        towers[tower_name] = {
            "weight": int(tower_weight[1:-1]),
            "sub_towers": sub_towers.split(", ") if sub_towers else [],
            "parent": None,
            "total_weight": None
        }

    for tower_name, tower_structure in towers.items():
        for sub_tower_name in tower_structure["sub_towers"]:
            towers[sub_tower_name]["parent"] = tower_name

    gen = (tower_name for tower_name, tower_structure in towers.items() if not tower_structure["parent"])
    bottom_tower = next(gen)

    determine_total_weight(towers, bottom_tower)

    return bottom_tower, find_weight_to_balance_tower(towers, bottom_tower)


def determine_total_weight(towers, tower_name):
    total_weight = towers[tower_name]["weight"]
    for sub_tower_name in towers[tower_name]["sub_towers"]:
        determine_total_weight(towers, sub_tower_name)
        total_weight += towers[sub_tower_name]["total_weight"]
    towers[tower_name]["total_weight"] = total_weight


def find_weight_to_balance_tower(towers, tower_name):
    if not towers[tower_name]["sub_towers"]:
        return None

    total_weights = [towers[sub_tower_name]["total_weight"] for sub_tower_name in towers[tower_name]["sub_towers"]]
    if all(tw == total_weights[0] for tw in total_weights):
        return None

    unbalanced_index = total_weights.index(max(total_weights))
    unbalanced_tower_name = towers[tower_name]["sub_towers"][unbalanced_index]
    weight_to_balance_tower = find_weight_to_balance_tower(towers, unbalanced_tower_name)
    if weight_to_balance_tower:
        return weight_to_balance_tower
    else:
        diff = max(total_weights) - min(total_weights)
        return towers[unbalanced_tower_name]["weight"] - diff


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    if os.path.isfile(test_input_file):
        with open(test_input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
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
