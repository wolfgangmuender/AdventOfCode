import os
import time
from collections import defaultdict
from copy import deepcopy


def solve(puzzle_input):
    initial_grove = PseudoMatrix(".")

    for line in puzzle_input:
        initial_grove.append_row(line)

    initial_grove.print()

    grove = initial_grove.copy()
    directions = ["N", "S", "W", "E"]

    proposals = None
    turns = 0
    for turn in range(0, 10):
        turns += 1
        proposals = do_turn(grove, directions)

    x_range = []
    y_range = []
    for x, y in grove.iter():
        if grove[x, y] != ".":
            if not x_range:
                x_range = [x, x]
            else:
                x_range[0] = min(x, x_range[0])
                x_range[1] = max(x, x_range[1])
            if not y_range:
                y_range = [y, y]
            else:
                y_range[0] = min(y, y_range[0])
                y_range[1] = max(y, y_range[1])

    num_empty = 0
    for x in range(x_range[0], x_range[1]+1):
        for y in range(y_range[0], y_range[1]+1):
            if grove[x, y] == ".":
                num_empty += 1

    print("Solution 1: {}".format(num_empty))

    while proposals:
        turns += 1
        proposals = do_turn(grove, directions)

    print("Solution 2: {}".format(turns))


def do_turn(grove, directions):
    proposals = {}
    for x, y in grove.iter():
        if grove[x, y] == "#":
            proposal = get_proposal(grove, directions, x, y)
            if proposal:
                proposals[get_key(x, y)] = proposal

    targets = list(proposals.values())
    for source, target in proposals.items():
        if targets.count(target) < 2:
            x, y = from_key(source)
            grove[x, y] = "."
            x, y = from_key(target)
            grove[x, y] = "#"

    directions.append(directions.pop(0))

    return proposals


def get_proposal(grove, directions, x, y):
    # N, NE, E, SE, S, SW, W, NW
    adj = [grove[x, y-1], grove[x+1, y-1], grove[x+1, y], grove[x+1, y+1], grove[x, y+1], grove[x-1, y+1], grove[x-1, y], grove[x-1, y-1]]
    if adj.count(".") == 8:
        return None

    for direction in directions:
        if direction == "N" and [adj[0], adj[1], adj[7]].count(".") == 3:
            return get_key(x, y - 1)
        if direction == "E" and [adj[1], adj[2], adj[3]].count(".") == 3:
            return get_key(x + 1, y)
        if direction == "S" and [adj[3], adj[4], adj[5]].count(".") == 3:
            return get_key(x, y + 1)
        if direction == "W" and [adj[5], adj[6], adj[7]].count(".") == 3:
            return get_key(x - 1, y)

    return None


def get_key(x, y):
    return f"{x}_{y}"


def from_key(key):
    return [int(k) for k in key.split("_")]


class PseudoMatrix:

    default_value = None
    data: dict
    x_range = []
    y_range = []

    def __init__(self, default_value=None):
        self.default_value = default_value
        if default_value:
            self.data = defaultdict(lambda: defaultdict(lambda: default_value))
        else:
            self.data = defaultdict(lambda: dict)

    def __getitem__(self, index):
        x, y = index
        return self.data[x][y]

    def __setitem__(self, index, value):
        x, y = index
        self.data[x][y] = value
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
            print(f"{y}".ljust(5) + "".join([self.data[x][y] for x in self.iter_x()]))

    def copy(self):
        the_copy = PseudoMatrix(self.default_value)
        the_copy.data = deepcopy(self.data)
        the_copy.x_range = deepcopy(self.x_range)
        the_copy.y_range = deepcopy(self.y_range)
        return the_copy

    def append_row(self, row):
        x = self.x_range[0] if self.x_range else 0
        y = self.y_range[1]+1 if self.y_range else 0
        for elem in row:
            self[x, y] = elem
            x += 1


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
