import os
import time
from collections import defaultdict
from copy import deepcopy

TEST_SOLUTION1 = "ABCDEF"
TEST_SOLUTION2 = 38


def solve(puzzle_input):
    routing_diagram = PseudoMatrix(" ")
    for line in puzzle_input:
        routing_diagram.append_row(line)

    x0 = None
    y0 = 0
    for x in routing_diagram.iter_x():
        if routing_diagram[x, y0] == "|":
            x0 = x

    letters = []

    x = x0
    y = y0
    x_diff = 0
    y_diff = 1
    steps = 1
    while routing_diagram[x + x_diff, y + y_diff] != " ":
        x += x_diff
        y += y_diff
        steps += 1
        if routing_diagram[x, y] in ["|", "-"]:
            continue
        elif routing_diagram[x, y] == "+":
            x_diff, y_diff = determine_direction(routing_diagram, x, y, x_diff, y_diff)
        else:
            letters.append(routing_diagram[x, y])

    return "".join(letters), steps


def determine_direction(routing_diagram, x, y, x_diff, y_diff):
    for diff in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        xd, yd = diff
        if xd == -x_diff and yd == -y_diff:
            continue
        if routing_diagram[x + xd, y + yd] != " ":
            return xd, yd

    raise Exception("Whoot?")


class PseudoMatrix:
    default_value = None
    data: dict
    x_range = []
    y_range = []

    def __init__(self, default_value=None):
        self.default_value = default_value
        if default_value is not None:
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
            print(f"{y}".ljust(5) + "".join([str(self.data[x][y]) for x in self.iter_x()]))

    def copy(self):
        the_copy = PseudoMatrix(self.default_value)
        the_copy.data = deepcopy(self.data)
        the_copy.x_range = deepcopy(self.x_range)
        the_copy.y_range = deepcopy(self.y_range)
        return the_copy

    def append_row(self, row):
        x = self.x_range[0] if self.x_range else 0
        y = self.y_range[1] + 1 if self.y_range else 0
        for elem in row:
            self[x, y] = elem
            x += 1


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    if os.path.isfile(test_input_file):
        with open(test_input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
        if solution1 != TEST_SOLUTION1:
            print(f"TEST solution 1 '{solution1}' not correct!")
            return
        if solution2 != TEST_SOLUTION2:
            print(f"TEST solution 2 '{solution2}' not correct!")
            return
        end = time.time()
        print_diff(end - start, True)
    else:
        open(test_input_file, 'a').close()

    input_file = "input/" + os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    if os.path.isfile(input_file):
        with open(input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
        print("Solution 1: {}".format(solution1))
        print("Solution 2: {}".format(solution2))
        end = time.time()
        print_diff(end - start, False)
    else:
        open(input_file, 'a').close()


def print_diff(diff, is_test):
    prefix = "TEST " if is_test else ""
    if diff >= 1:
        print("The {}solutions took {}s".format(prefix, round(diff)))
    else:
        print("The {}solutions took {}ms".format(prefix, round(diff * 1000)))


if __name__ == "__main__":
    main()
