import os
import time
from copy import deepcopy


def main(puzzle_input):
    instructions = []
    for line in puzzle_input:
        if line.startswith("addx"):
            instructions.append(int(line[4:]))
        else:
            instructions.append(None)

    instructions_1 = deepcopy(instructions)

    x = 1
    add_x = None
    cycle_x = []
    cycle = 0
    while cycle < 240:
        cycle_x.append(x)

        if add_x:
            x += add_x
            add_x = None
        else:
            instruction = instructions_1.pop(0)
            if instruction:
                add_x = instruction

        cycle += 1

    print("Solution 1: {}".format(_sum(cycle_x)))

    pixels = []
    cycle = 0
    while cycle < 240:
        pixels.append("#" if abs(cycle_x[cycle] - (cycle % 40)) <= 1 else ".")
        cycle += 1

    print("".join(pixels[0:40]))
    print("".join(pixels[40:80]))
    print("".join(pixels[80:120]))
    print("".join(pixels[120:160]))
    print("".join(pixels[160:200]))
    print("".join(pixels[200:240]))

    print("Solution 2: {}".format("ERCREPCJ"))


def _sum(cycle_x):
    return 20*cycle_x[19] + 60*cycle_x[59] + 100*cycle_x[99] + 140*cycle_x[139] + 180*cycle_x[179] + 220*cycle_x[219]


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
