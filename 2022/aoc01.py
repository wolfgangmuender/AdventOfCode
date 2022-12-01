import os
import time


def main(puzzle_input):
    elf_packs = [[]]
    for ration in puzzle_input:
        if ration:
            elf_packs[-1].append(int(ration))
        else:
            elf_packs.append([])

    total_rations = [sum(elf_pack) for elf_pack in elf_packs]
    total_rations.sort(reverse=True)

    print("Solution 1: the elf with the most Calories is carrying {} Calories".format(total_rations[0]))
    print("Solution 2: the three elves with the most Calories are carrying {} Calories in total".format(sum(total_rations[0:3])))


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
