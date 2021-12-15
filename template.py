import os
import time


def main(puzzle_input):
    print("Solution 1: {}".format(0))
    print("Solution 2: {}".format(0))


if __name__ == "__main__":
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    main(content)
    end = time.time()
    print("The solutions took {} seconds".format(end - start))
