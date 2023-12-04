import os
import time

TEST_SOLUTION1 = 13
TEST_SOLUTION2 = 30


def solve(puzzle_input):
    cards = []
    for line in puzzle_input:
        card_id_str, numbers = line.split(": ")
        winning_numbers_str, own_numbers_str = numbers.split(" | ")

        card_id = int(card_id_str.replace("Card ", ""))
        winning_numbers = {int(w) for w in winning_numbers_str.split(" ") if w}
        own_numbers = {int(o) for o in own_numbers_str.split(" ") if o}

        matches = len(own_numbers & winning_numbers)

        cards.append({
            "id": card_id,
            "winning_numbers": winning_numbers,
            "own_numbers": own_numbers,
            "matches": matches,
            "points": pow(2, matches - 1) if matches else 0,
        })

    card_nums = {card["id"]: 1 for card in cards}
    for card in cards:
        curr = card["id"]
        for won in range(curr + 1, curr + card["matches"] + 1):
            card_nums[won] += card_nums[curr]

    return sum([c["points"] for c in cards]), sum(card_nums.values())


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
