import os
import time
from collections import defaultdict
from copy import deepcopy


def solve(puzzle_input):
    initial_blizzards = PseudoMatrix(".")
    y = 0
    for line in puzzle_input:
        if line.count("#") == 2:
            x = 0
            for char in line[1:-1]:
                if char != "#":
                    initial_blizzards[x, y] = char
                    x += 1
            y += 1

    max_x = len(puzzle_input[0]) - 3
    max_y = len(puzzle_input) - 3

    blizzards_per_minute = {0: initial_blizzards}

    there = travel(blizzards_per_minute, max_x, max_y, {"pos": [0, -1], "minute": 0}, [max_x, max_y])

    print("Solution 1: {}".format(there))

    back = travel(blizzards_per_minute, max_x, max_y, {"pos": [max_x, max_y+1], "minute": there}, [0, 0])
    there_again = travel(blizzards_per_minute, max_x, max_y, {"pos": [0, -1], "minute": back}, [max_x, max_y])

    print("Solution 2: {}".format(there_again))


def travel(blizzards_per_minute, max_x, max_y, start, end):
    def dist(p): return abs(end[0] - p["pos"][0]) + abs(end[1] - p["pos"][1])

    shortest_time = None
    candidates = [start]
    cache = []
    rounds = 0
    while candidates:
        rounds += 1
        if rounds % 100000 == 0:
            print(rounds)
            print(len(candidates))

        curr_path = min(candidates, key=dist)
        candidates.remove(curr_path)

        if shortest_time and curr_path["minute"] + dist(curr_path) >= shortest_time:
            continue

        if get_key(curr_path) in cache:
            continue
        else:
            cache.append(get_key(curr_path))

        next_minute = curr_path["minute"] + 1
        blizzards = get_blizzards(blizzards_per_minute, next_minute)

        if curr_path["pos"] == end:
            shortest_time = next_minute
            print(curr_path)
            candidates = [candidate for candidate in candidates if candidate["minute"] + dist(candidate) < shortest_time]
            continue

        x = curr_path["pos"][0]
        y = curr_path["pos"][1]
        if blizzards[x, y] == ".":
            candidates.append({
                "pos": [x, y],
                "minute": next_minute
            })
        if y > 0 and blizzards[x, y-1] == ".":
            candidates.append({
                "pos": [x, y-1],
                "minute": next_minute
            })
        if y < max_y and blizzards[x, y+1] == ".":
            candidates.append({
                "pos": [x, y+1],
                "minute": next_minute
            })
        if 0 <= y <= max_y and x < max_x and blizzards[x+1, y] == ".":
            candidates.append({
                "pos": [x+1, y],
                "minute": next_minute
            })
        if 0 <= y <= max_y and x > 0 and blizzards[x-1, y] == ".":
            candidates.append({
                "pos": [x-1, y],
                "minute": next_minute
            })

    return shortest_time


def get_blizzards(blizzards_per_minute, minute):
    if minute in blizzards_per_minute:
        return blizzards_per_minute[minute]
    else:
        old_blizzards = blizzards_per_minute[minute - 1]
        blizzards = PseudoMatrix(".", old_blizzards.x_range, old_blizzards.y_range)
        for x, y in old_blizzards.iter():
            if old_blizzards[x, y] != ".":
                for direction in old_blizzards[x, y]:
                    if direction == "^":
                        x2, y2 = x, y - 1
                    elif direction == "v":
                        x2, y2 = x, y + 1
                    elif direction == ">":
                        x2, y2 = x + 1, y
                    elif direction == "<":
                        x2, y2 = x - 1, y
                    else:
                        raise Exception("Whoot?")

                    x2 = x2 if x2 >= old_blizzards.x_range[0] else old_blizzards.x_range[1]
                    x2 = x2 if x2 <= old_blizzards.x_range[1] else old_blizzards.x_range[0]
                    y2 = y2 if y2 >= old_blizzards.y_range[0] else old_blizzards.y_range[1]
                    y2 = y2 if y2 <= old_blizzards.y_range[1] else old_blizzards.y_range[0]

                    blizzards[x2, y2] = direction

        blizzards_per_minute[minute] = blizzards

        return blizzards


def get_key(path):
    return f"{path['pos'][0]}_{path['pos'][1]}_{path['minute']}"


class PseudoMatrix:
    default_value = None
    data: dict
    x_range = []
    y_range = []

    def __init__(self, default_value=None, x_range=None, y_range=None):
        self.default_value = default_value
        if default_value:
            self.data = defaultdict(lambda: defaultdict(lambda: default_value))
        else:
            self.data = defaultdict(lambda: dict)
        self.x_range = x_range
        self.y_range = y_range

    def __getitem__(self, index):
        x, y = index
        return self.data[x][y]

    def __setitem__(self, index, value):
        x, y = index
        self.data[x][y] = value if self.data[x][y] == "." else self.data[x][y] + value
        self._update_range(x, y)

    def _update_range(self, x, y):
        if self.x_range:
            self.x_range[0] = min(self.x_range[0], x)
            self.x_range[1] = max(self.x_range[1], x)
        else:
            self.x_range = [x, x]

        if self.y_range:
            self.y_range[0] = min(self.y_range[0], y)
            self.y_range[1] = max(self.y_range[1], y)
        else:
            self.y_range = [y, y]

    def iter_x(self):
        for x in range(self.x_range[0], self.x_range[1] + 1):
            yield x

    def iter_y(self):
        for y in range(self.y_range[0], self.y_range[1] + 1):
            yield y

    def iter(self):
        for y in range(self.y_range[0], self.y_range[1] + 1):
            for x in range(self.x_range[0], self.x_range[1] + 1):
                yield x, y

    def print(self):
        for y in self.iter_y():
            print(f"{y}".ljust(5) + "".join([self.data[x][y] if len(self.data[x][y]) == 1 else str(len(self.data[x][y])) for x in self.iter_x()]))


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
