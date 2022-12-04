import os
import time


def main(puzzle_input):
    section_pairs = []
    for line in puzzle_input:
        elves = line.split(",")
        section_pairs.append([_convert(elves[0]), _convert(elves[1])])

    fully_containing = sum([_check(section_pair, _fully_containing) for section_pair in section_pairs])
    print("Solution 1: the number of fully overlapping pairs is {}".format(fully_containing))

    overlapping = sum([_check(section_pair, _overlapping) for section_pair in section_pairs])
    print("Solution 2: the number of overlapping pairs is {}".format(overlapping))


def _convert(range_input):
    return [int(num) for num in range_input.split("-")]


def _check(section_pair, check_fun):
    elf1 = section_pair[0]
    elf2 = section_pair[1]
    return 1 if check_fun(elf1, elf2) or check_fun(elf2, elf1) else 0


def _fully_containing(elf1, elf2):
    return elf1[0] <= elf2[0] and elf1[1] >= elf2[1]


def _overlapping(elf1, elf2):
    return elf1[0] <= elf2[0] <= elf1[1] or elf1[0] <= elf2[1] <= elf1[1]


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
