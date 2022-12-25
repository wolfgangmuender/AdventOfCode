import os
import time
from math import ceil, log

SNAFU_TO_NUMERAL = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}


def solve(puzzle_input):
    snafu_numbers = [line for line in puzzle_input]

    numbers = []
    for snafu_number in snafu_numbers:
        number = 0
        digit = 0
        for snafu_numeral in snafu_number[-1::-1]:
            number += SNAFU_TO_NUMERAL[snafu_numeral] * 5 ** digit
            digit += 1
        numbers.append(number)

    print("Solution 1: {}".format(decimal_to_snafu(sum(numbers))))


def decimal_to_snafu(number):
    if number < 0:
        raise Exception("Whoot?")

    snafu_number = []
    curr_number = number
    curr_pow = ceil(log(number, 5))
    while curr_pow >= 0:
        if 0.5 * 5**curr_pow < abs(curr_number) < 1.5 * 5**curr_pow:
            sign = 1 if curr_number > 0 else -1
            snafu_number.append("1" if sign > 0 else "-")
            curr_number -= sign * 5**curr_pow
            curr_pow -= 1
        elif 1.5 * 5**curr_pow < abs(curr_number) < 2.5 * 5**curr_pow:
            sign = 1 if curr_number > 0 else -1
            snafu_number.append("2" if sign > 0 else "=")
            curr_number -= sign * 2 * 5**curr_pow
            curr_pow -= 1
        else:
            snafu_number.append("0")
            curr_pow -= 1

    while snafu_number[0] == "0":
        snafu_number.pop(0)

    return "".join(snafu_number)


def main():
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    solve(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))


if __name__ == "__main__":
    main()
