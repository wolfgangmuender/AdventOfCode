import os
import time
from copy import deepcopy

TEST_SOLUTION1 = 19114
TEST_SOLUTION2 = 167409079868000


def solve(puzzle_input):
    workflows = {}
    parts = []
    for line in puzzle_input:
        if line.startswith("{"):
            part = {}
            categories_str = line[1:-1].split(",")
            for category_str in categories_str:
                category, value_str = category_str.split("=")
                part[category] = int(value_str)
            parts.append(part)
        elif line:
            name, rules_list = line[:-1].split("{")
            rules = []
            default = None
            targets = []
            for rule_str in rules_list.split(","):
                if ":" in rule_str:
                    condition, target = rule_str.split(":")
                    rules.append({
                        "condition": [condition[0], condition[1], int(condition[2:])],
                        "target": target,
                    })
                    targets.append(target)
                else:
                    default = rule_str
                    targets.append(default)
            workflows[name] = {
                "rules": rules if len(set(targets)) > 1 else [],
                "default": default,
            }

    total_rating = 0
    for part in parts:
        workflow_name = "in"
        while workflow_name not in ["A", "R"]:
            workflow_name = apply_workflow(part, workflows[workflow_name])
        if workflow_name == "A":
            total_rating += part["x"] + part["m"] + part["a"] + part["s"]

    part_ranges = [{
        "x": [1, 4000],
        "m": [1, 4000],
        "a": [1, 4000],
        "s": [1, 4000],
        "workflow": "in",
    }]
    part_ranges_final = []
    while part_ranges:
        part_range = part_ranges.pop()
        new_part_ranges = apply_workflow_to_range(part_range, workflows[part_range["workflow"]])
        for new_part_range in new_part_ranges:
            if new_part_range["workflow"] == "A":
                part_ranges_final.append(new_part_range)
            elif new_part_range["workflow"] != "R":
                part_ranges.append(new_part_range)

    return total_rating, sum([count_combinations(part_range) for part_range in part_ranges_final])


def apply_workflow(part, workflow):
    for rule in workflow["rules"]:
        category = rule["condition"][0]
        comparator = rule["condition"][1]
        value = rule["condition"][2]
        if comparator == ">":
            if part[category] > value:
                return rule["target"]
        if comparator == "<":
            if part[category] < value:
                return rule["target"]
    return workflow["default"]


def apply_workflow_to_range(part_range, workflow):
    new_part_ranges = []

    for rule in workflow["rules"]:
        category = rule["condition"][0]
        comparator = rule["condition"][1]
        value = rule["condition"][2]
        if comparator == ">":
            cat0 = part_range[category][0]
            cat1 = part_range[category][1]
            if cat0 > value:
                part_range["workflow"] = rule["target"]
                new_part_ranges.append(part_range)
                return new_part_ranges
            elif cat0 == value:
                raise Exception("I don't want to think about this!")
            elif cat0 < value < cat1:
                new_part_range = deepcopy(part_range)
                new_part_range["workflow"] = rule["target"]
                new_part_ranges.append(new_part_range)
                part_range[category] = [cat0, value]
                new_part_range[category] = [value + 1, cat1]
        if comparator == "<":
            cat0 = part_range[category][0]
            cat1 = part_range[category][1]
            if cat1 < value:
                part_range["workflow"] = rule["target"]
                new_part_ranges.append(part_range)
                return new_part_ranges
            elif cat1 == value:
                raise Exception("I don't want to think about this!")
            elif cat0 < value < cat1:
                new_part_range = deepcopy(part_range)
                new_part_range["workflow"] = rule["target"]
                new_part_ranges.append(new_part_range)
                part_range[category] = [value, cat1]
                new_part_range[category] = [cat0, value - 1]

    part_range["workflow"] = workflow["default"]
    new_part_ranges.append(part_range)

    return new_part_ranges


def count_combinations(part_range):
    count = 1
    for cat in ["x", "m", "a", "s"]:
        count *= (part_range[cat][1] - part_range[cat][0] + 1)
    return count


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
