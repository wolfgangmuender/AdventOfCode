import math
import os
import time

TEST_SOLUTION1 = 65
TEST_SOLUTION2 = 188

WEAPONS = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
ARMOR = [(0, 0, 0), (13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]
RINGS = [(0, 0, 0), (25, 1, 0), (50, 2, 0), (100, 3, 0), (20, 0, 1), (40, 0, 2), (80, 0, 3)]


def solve(puzzle_input):
    boss_stats = []
    for line in puzzle_input:
        _, stat = line.split(": ")
        boss_stats.append(int(stat))

    hit_points = 100 if boss_stats[0] > 100 else 8

    min_gold = 1000
    max_gold = 0
    for weapon in WEAPONS:
        for armor in ARMOR:
            for i in range(0, len(RINGS)):
                ring1 = RINGS[i]
                for j in range(i, len(RINGS)):
                    if i > 0 and i == j:
                        continue
                    ring2 = RINGS[j]
                    gold = weapon[0] + armor[0] + ring1[0] + ring2[0]
                    if fight(hit_points, weapon[1] + armor[1] + ring1[1] + ring2[1], weapon[2] + armor[2] + ring1[2] + ring2[2], *boss_stats):
                        min_gold = min(gold, min_gold)
                    else:
                        max_gold = max(gold, max_gold)


    return min_gold, max_gold


def fight(hit_points, damage, armor, boss_hit_points, boss_damage, boss_armor):
    win = math.ceil(boss_hit_points / max(damage - boss_armor, 1)) <= math.ceil(hit_points / max(boss_damage - armor, 1))
    print(win)
    return win


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
