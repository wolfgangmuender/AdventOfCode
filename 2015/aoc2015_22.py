import os
import time
from copy import copy

TEST_SOLUTION1 = 246
TEST_SOLUTION2 = 588

SPELLS = []


def solve(puzzle_input):
    boss_stats = []
    for line in puzzle_input:
        _, stat = line.split(": ")
        boss_stats.append(int(stat))

    initial_state = {
        "hit_points": 50 if boss_stats[0] > 50 else 15,
        "mana": 500 if boss_stats[0] > 50 else 250,
        "shield": 0,
        "poison": 0,
        "recharge": 0,
        "boss_hit_points": boss_stats[0],
        "boss_damage": boss_stats[1],
        "player_turn": True,
        "mana_spent": 0
    }

    minimal_mana = fight(initial_state, 1000000, False)
    minimal_mana_hard = fight(initial_state, 1000000, True)

    return minimal_mana, minimal_mana_hard


def fight(state, minimal_mana, is_hard):
    if state["mana_spent"] >= minimal_mana:
        return minimal_mana

    if is_hard and state["player_turn"]:
        state["hit_points"] -= 1
        if state["hit_points"] <= 0:
            return minimal_mana

    if state["shield"]:
        state["shield"] -= 1

    if state["poison"]:
        state["boss_hit_points"] -= 3
        if state["boss_hit_points"] <= 0:
            return min(minimal_mana, state["mana_spent"])
        state["poison"] -= 1

    if state["recharge"]:
        state["mana"] += 101
        state["recharge"] -= 1

    new_minimal_mana = minimal_mana
    if state["player_turn"]:
        if state["mana"] >= 53:
            new_state = copy(state)
            new_state["mana"] -= 53
            new_state["mana_spent"] += 53
            new_state["boss_hit_points"] -= 4
            if new_state["boss_hit_points"] <= 0:
                new_minimal_mana = min(new_minimal_mana, new_state["mana_spent"])
            else:
                new_state["player_turn"] = False
                new_minimal_mana = min(new_minimal_mana, fight(new_state, new_minimal_mana, is_hard))

        if state["mana"] >= 73:
            new_state = copy(state)
            new_state["mana"] -= 73
            new_state["mana_spent"] += 73
            new_state["boss_hit_points"] -= 2
            new_state["hit_points"] += 2
            if new_state["boss_hit_points"] <= 0:
                new_minimal_mana = min(new_minimal_mana, new_state["mana_spent"])
            else:
                new_state["player_turn"] = False
                new_minimal_mana = min(new_minimal_mana, fight(new_state, new_minimal_mana, is_hard))

        if state["mana"] >= 113:
            new_state = copy(state)
            new_state["mana"] -= 113
            new_state["mana_spent"] += 113
            new_state["shield"] = 6
            new_state["player_turn"] = False
            new_minimal_mana = min(new_minimal_mana, fight(new_state, new_minimal_mana, is_hard))

        if state["mana"] >= 173:
            new_state = copy(state)
            new_state["mana"] -= 173
            new_state["mana_spent"] += 173
            new_state["poison"] = 6
            new_state["player_turn"] = False
            new_minimal_mana = min(new_minimal_mana, fight(new_state, new_minimal_mana, is_hard))

        if state["mana"] >= 229:
            new_state = copy(state)
            new_state["mana"] -= 229
            new_state["mana_spent"] += 229
            new_state["recharge"] = 5
            new_state["player_turn"] = False
            new_minimal_mana = min(new_minimal_mana, fight(new_state, new_minimal_mana, is_hard))
    else:
        armor = 7 if state["shield"] else 0
        state["hit_points"] -= max(state["boss_damage"] - armor, 1)
        if state["hit_points"] > 0:
            state["player_turn"] = True
            new_minimal_mana = min(new_minimal_mana, fight(state, new_minimal_mana, is_hard))

    return new_minimal_mana


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
