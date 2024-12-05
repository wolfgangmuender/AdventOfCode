import os
import time

TEST_SOLUTION1 = 143
TEST_SOLUTION2 = 123


def solve(puzzle_input):
    rules = []
    updates = []
    for line in puzzle_input:
        if "|" in line:
            r1, r2 = [int(n) for n in line.split("|")]
            rules.append([r1, r2])
        elif "," in line:
            updates.append([int(n) for n in line.split(",")])

    correct_updates = []
    fixed_updates = []
    for update in updates:
        is_correct = True
        for rule in rules:
            r1, r2 = rule
            if r1 in update and r2 in update and not update.index(r1) < update.index(r2):
                is_correct = False
                break
        if is_correct:
            correct_updates.append(update)
        else:
            fixed_updates.append(fix_update(update, rules))

    correct_middle_number_sum = sum([update[len(update) // 2] for update in correct_updates])
    fixed_middle_number_sum = sum([update[len(update) // 2] for update in fixed_updates])

    return correct_middle_number_sum, fixed_middle_number_sum


def fix_update(update, rules):
    fixed_update = []

    for p1 in update:
        if len(fixed_update) == 0:
            fixed_update.append(p1)
        else:
            inserted = False
            for i in range(0, len(fixed_update)):
                p2 = fixed_update[i]
                if check_rules(p1, p2 , rules):
                    fixed_update.insert(i, p1)
                    inserted = True
                    break
            if not inserted:
                fixed_update.append(p1)

    return fixed_update

def check_rules(p1, p2, rules):
    for rule in rules:
        r1, r2 = rule
        if r1 == p1 and r2 == p2:
            return True
    return False


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
