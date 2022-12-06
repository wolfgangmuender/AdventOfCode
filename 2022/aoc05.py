import os
import time
from copy import deepcopy


def main(puzzle_input):
    initial_stacks = []
    steps = []
    for line in puzzle_input:
        if line.startswith("move"):
            step_str = line.replace("move ", "").replace(" from", "").replace(" to", "")
            steps.append([int(s) for s in step_str.split(" ")])
        elif line and not line.startswith(" 1"):
            crates = line[1::4]
            stack_pos = 0
            for crate in crates:
                if len(initial_stacks) <= stack_pos:
                    initial_stacks.append([])
                if crate != " ":
                    initial_stacks[stack_pos].insert(0, crate)
                stack_pos += 1

    stacks = deepcopy(initial_stacks)
    for step in steps:
        for i in range(0, step[0]):
            crate = stacks[step[1]-1].pop()
            stacks[step[2]-1].append(crate)

    print("Solution 1: {}".format("".join([x[-1] for x in stacks])))

    stacks = deepcopy(initial_stacks)
    for step in steps:
        crates = []
        for i in range(0, step[0]):
            crate = stacks[step[1]-1].pop()
            crates.insert(0, crate)
        stacks[step[2]-1].extend(crates)

    print("Solution 2: {}".format("".join([x[-1] for x in stacks])))


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
