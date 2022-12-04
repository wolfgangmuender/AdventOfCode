import os
import time


ABC = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def main(puzzle_input):
    rucksacks = []
    for line in puzzle_input:
        rucksacks.append(line)

    priorities = []
    for rucksack in rucksacks:
        compartment1, compartment2 = rucksack[:len(rucksack) // 2], rucksack[len(rucksack) // 2:]
        common_type = list(set(compartment1) & set(compartment2))[0]
        priorities.append(ABC.index(common_type)+1)

    print("Solution 1: the sum of the priorities is {}".format(sum(priorities)))

    priorities = []
    for i in range(0, len(rucksacks), 3):
        common_type = list(set(rucksacks[i]) & set(rucksacks[i+1]) & set(rucksacks[i+2]))[0]
        priorities.append(ABC.index(common_type)+1)

    print("Solution 2: the sum of the priorities is {}".format(sum(priorities)))


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
