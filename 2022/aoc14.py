import os
import time
from collections import defaultdict
from copy import deepcopy


def main(puzzle_input):
    cave_map = defaultdict(lambda: defaultdict(lambda: "."))
    max_y = 0
    for line in puzzle_input:
        points = line.split(" -> ")
        for i in range(0, len(points)-1):
            x1, y1 = [int(p) for p in points[i].split(",")]
            x2, y2 = [int(p) for p in points[i+1].split(",")]
            if x1 == x2:
                yf = min(y1, y2)
                yt = max(y1, y2)
                for y in range(yf, yt+1):
                    cave_map[x1][y] = "#"
            elif y1 == y2:
                xf = min(x1, x2)
                xt = max(x1, x2)
                for x in range(xf, xt+1):
                    cave_map[x][y1] = "#"
            else:
                raise Exception("Whoot?")
            max_y = max(max_y, y1, y2)

    _print(cave_map, max_y)

    cave_map1 = deepcopy(cave_map)
    sand_units1 = 0
    while _flow(cave_map1, max_y, True):
        sand_units1 += 1

    _print(cave_map1, max_y)
    print("Solution 1: {}".format(sand_units1))

    cave_map2 = deepcopy(cave_map)
    sand_units2 = 0
    while cave_map2[500][0] != "o":
        _flow(cave_map2, max_y+1, False)
        sand_units2 += 1

    _print(cave_map2, max_y+1)
    print("Solution 2: {}".format(sand_units2))


def _flow(cave_map, max_y, bottomless):
    x, y = 500, 0
    while y < max_y:
        if cave_map[x][y+1] == ".":
            y += 1
        elif cave_map[x-1][y+1] == ".":
            x -= 1
            y += 1
        elif cave_map[x+1][y+1] == ".":
            x += 1
            y += 1
        else:
            cave_map[x][y] = "o"
            return True

    if bottomless:
        return False
    else:
        cave_map[x][y] = "o"
        return True


def _print(cave_map, max_y):
    min_x = min(cave_map.keys())
    max_x = max(cave_map.keys())
    print("".join(["=" for x in range(min_x, max_x + 1)]))
    for y in range(0, max_y + 1):
        print("".join([cave_map[x][y] for x in range(min_x, max_x+1)]))


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
