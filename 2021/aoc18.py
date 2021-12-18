import math
import os
import time
from copy import deepcopy


def main(puzzle_input):
    snailfish_numbers = [eval(line) for line in puzzle_input]

    final_sum = None
    for i in range(0, len(snailfish_numbers)):
        next_number = deepcopy(snailfish_numbers[i])
        if final_sum:
            final_sum = [final_sum, next_number]
        else:
            final_sum = next_number
        reduce(final_sum)

    print("Solution 1: the magnitude of the final sum is {}".format(get_magnitude(final_sum)))

    magnitudes = []
    for i in range(0, len(snailfish_numbers)):
        for j in range(0, len(snailfish_numbers)):
            if i != j:
                the_sum = [deepcopy(snailfish_numbers[i]), deepcopy(snailfish_numbers[j])]
                reduce(the_sum)
                magnitudes.append(get_magnitude(the_sum))

    print("Solution 2: the largest magnitude of any sum of two different snailfish numbers is {}"
          .format(max(magnitudes)))


def reduce(snailfish_number):
    action_taken = None
    while action_taken is None or action_taken:
        action_taken = explode(snailfish_number, 0, {}) or split(snailfish_number)


def explode(snailfish_number, depth, state):
    exploded = False

    for i in range(0, 2):
        if isinstance(snailfish_number[i], list):
            if "add_to_right" in state:
                return explode(snailfish_number[i], depth + 1, state)
            elif not exploded:
                if depth < 3:
                    exploded = explode(snailfish_number[i], depth + 1, state)
                else:
                    if "left" in state:
                        state["left"][state["left_index"]] = state["left"][state["left_index"]] + snailfish_number[i][0]
                    state["add_to_right"] = snailfish_number[i][1]
                    snailfish_number[i] = 0
                    exploded = True
        else:
            if "add_to_right" in state:
                snailfish_number[i] = snailfish_number[i] + state["add_to_right"]
                del state["add_to_right"]
                return True
            elif not exploded:
                state["left"] = snailfish_number
                state["left_index"] = i

    return exploded


def split(snailfish_number):
    for i in range(0, 2):
        if isinstance(snailfish_number[i], list):
            if split(snailfish_number[i]):
                return True
        else:
            if snailfish_number[i] > 9:
                snailfish_number[i] = [math.floor(snailfish_number[i] / 2), math.ceil(snailfish_number[i] / 2)]
                return True

    return False


def get_magnitude(snailfish_number):
    left = get_magnitude(snailfish_number[0]) if isinstance(snailfish_number[0], list) else snailfish_number[0]
    right = get_magnitude(snailfish_number[1]) if isinstance(snailfish_number[1], list) else snailfish_number[1]

    return 3 * left + 2 * right


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
