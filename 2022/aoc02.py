import os
import time


SCORES_1 = {
    "A X": 4,
    "A Y": 8,
    "A Z": 3,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 7,
    "C Y": 2,
    "C Z": 6,
}

# A Stein 1
# B Papier 2
# C Schere 3

SCORES_2 = {
    "A X": 3,
    "A Y": 4,
    "A Z": 8,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 2,
    "C Y": 6,
    "C Z": 7,
}


def main(puzzle_input):
    score_1 = sum([SCORES_1[game] for game in puzzle_input])
    print("Solution 1: the total score using the wrong strategy is {}".format(score_1))

    score_2 = sum([SCORES_2[game] for game in puzzle_input])
    print("Solution 2: the total score using the correct strategy is {}".format(score_2))


if __name__ == "__main__":
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    main(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))
