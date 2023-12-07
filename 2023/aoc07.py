import os
import time
from collections import defaultdict
from copy import copy

TEST_SOLUTION1 = 6440
TEST_SOLUTION2 = 5905

CARD_MAP = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14
}
CARD_MAP_JOKER = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 1, "Q": 12, "K": 13, "A": 14
}


def solve(puzzle_input):
    hands = read_hands(puzzle_input, False)
    hands_joker = read_hands(puzzle_input, True)

    total_score = sum([(i + 1) * hands[i]["bit"] for i in range(0, len(hands))])
    total_score_joker = sum([(i + 1) * hands_joker[i]["bit"] for i in range(0, len(hands_joker))])

    return total_score, total_score_joker


def read_hands(puzzle_input, use_joker):
    card_map = CARD_MAP_JOKER if use_joker else CARD_MAP
    hands = []
    for line in puzzle_input:
        cards = [card_map[line[i]] for i in range(0, 5)]
        bit = int(line[6:])
        hands.append({
            "cards": cards,
            "card_value": get_cards_value(cards),
            "bit": bit,
            "strength": decide_strength(cards, use_joker),
        })
    hands.sort(key=lambda x: x["strength"] + x["card_value"] / pow(10, 10))
    return hands


def get_cards_value(cards):
    return pow(10, 8) * cards[0] + pow(10, 6) * cards[1] + pow(10, 4) * cards[2] + pow(10, 2) * cards[3] + cards[4]


def decide_strength(cards, use_joker):
    grouped = defaultdict(lambda: 0)
    for card in cards:
        grouped[card] += 1
    gv = [v for v in grouped.values()]
    if use_joker:
        num_jokers = grouped[1]
        if max(gv) == 5:
            return 7
        elif max(gv) == 4:
            if num_jokers:
                return 7
            else:
                return 6
        elif max(gv) == 3 and len(gv) == 2:
            if num_jokers:
                return 7
            else:
                return 5
        elif max(gv) == 3 and len(gv) == 3:
            if num_jokers:
                return 6
            else:
                return 4
        elif max(gv) == 2 and len(gv) == 3:
            if num_jokers == 2:
                return 6
            elif num_jokers == 1:
                return 5
            else:
                return 3
        elif max(gv) == 2 and len(gv) == 4:
            if num_jokers:
                return 4
            else:
                return 2
        else:
            if num_jokers:
                return 2
            else:
                return 1
    else:
        if max(gv) == 5:
            return 7
        elif max(gv) == 4:
            return 6
        elif max(gv) == 3 and len(gv) == 2:
            return 5
        elif max(gv) == 3 and len(gv) == 3:
            return 4
        elif max(gv) == 2 and len(gv) == 3:
            return 3
        elif max(gv) == 2 and len(gv) == 4:
            return 2
        else:
            return 1


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
