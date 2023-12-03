import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 8
TEST_SOLUTION2 = 2286


def solve(puzzle_input):
    games = {}
    for line in puzzle_input:
        game_id_str, probes_str = line.split(": ")
        game_id = int(game_id_str.replace("Game ", ""))
        game_impossible = False
        min_red = 0
        min_green = 0
        min_blue = 0
        for probes in probes_str.split("; "):
            for probe in probes.split(", "):
                num_str, color = probe.split(" ")
                num = int(num_str)
                if color == "red":
                    min_red = max(min_red, num)
                    if num > 12:
                        game_impossible = True
                if color == "green":
                    min_green = max(min_green, num)
                    if num > 13:
                        game_impossible = True
                if color == "blue":
                    min_blue = max(min_blue, num)
                    if num > 14:
                        game_impossible = True
        games[game_id] = {
            "game_impossible": game_impossible,
            "power": min_red * min_green * min_blue
        }

    return sum([game_id for game_id, game in games.items() if not game["game_impossible"]]), sum([game["power"] for game in games.values()])


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
