import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 37327623
TEST_SOLUTION2 = 24


def solve(puzzle_input):
    initial_secrets = []
    for line in puzzle_input:
        initial_secrets.append(int(line))

    final_secrets = []
    all_price_mappings = []
    for initial_secret in initial_secrets:
        prices = []
        evolved_secret = initial_secret
        for i in range(0, 2000):
            evolved_secret = evolve(evolved_secret)
            prices.append(evolved_secret % 10)

        price_changes = [prices[i] - prices[i - 1] if i > 0 else prices[i] - (initial_secret % 10) for i in range(0, len(prices))]
        price_mapping = defaultdict(lambda: 0)
        for i in range(4, len(prices)):
            monkey_command = tuple(price_changes[i - 4:i])
            if monkey_command not in price_mapping:
                price_mapping[monkey_command] = prices[i - 1]

        final_secrets.append(evolved_secret)
        all_price_mappings.append(price_mapping)

    monkey_command_map = {}
    for monkey_command in get_monkey_commands(all_price_mappings):
        monkey_command_map[monkey_command] = sum([price_mapping[monkey_command] for price_mapping in all_price_mappings])

    return sum(final_secrets), max(monkey_command_map.values())


def evolve(secret):
    evolved_secret = (secret ^ (secret * 64)) % 16777216
    evolved_secret = (evolved_secret ^ int(evolved_secret / 32)) % 16777216
    evolved_secret = (evolved_secret ^ (evolved_secret * 2048)) % 16777216
    return evolved_secret


def get_monkey_commands(all_price_mappings):
    monkey_commands = set()
    for price_mapping in all_price_mappings:
        monkey_commands.update(price_mapping.keys())
    return monkey_commands


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
