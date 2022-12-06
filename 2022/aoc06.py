import os
import time


def main(puzzle_input):
    datastream = puzzle_input[0]

    print("Solution 1: {}".format(find_marker(datastream, 4)))
    print("Solution 2: {}".format(find_marker(datastream, 14)))


def find_marker(datastream, length):
    processed = 0
    marker = []
    for c in datastream:
        processed += 1
        if len(marker) == length:
            marker.pop(0)
        marker.append(c)
        if len(set(marker)) == length:
            break

    return processed


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
