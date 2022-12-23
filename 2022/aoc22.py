import os
import time
from collections import defaultdict


DIRECTIONS = ">v<^"


def solve(puzzle_input):
    board = PseudoMatrix(" ")
    path = None

    y = 1
    for line in puzzle_input:
        if not line:
            y = None
        elif y:
            x = 1
            for char in line:
                board[x, y] = char
                x += 1
            y += 1
        else:
            path = line

    x_initial, y_initial, _, _ = board.get_next(1, 1, ">")

    x, y, direction = trace(board, path, x_initial, y_initial)

    print("Solution 1: {}".format(4*x + 1000*y + DIRECTIONS.index(direction)))

    board.do_wrap_3d()
    x, y, direction = trace(board, path, x_initial, y_initial)

    print("Solution 1: {}".format(4*x + 1000*y + DIRECTIONS.index(direction)))


def trace(board, path, x_initial, y_initial):
    x, y, direction = x_initial, y_initial, ">"
    curr_num_str = None
    for i in range(0, len(path)):
        char = path[i]
        if char == "L":
            direction = DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]
            curr_num_str = None
        elif char == "R":
            direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]
            curr_num_str = None
        else:
            curr_num_str = curr_num_str + char if curr_num_str else char
            if i == len(path)-1 or path[i+1] in ["L", "R"]:
                curr_num = int(curr_num_str)
                for j in range(0, curr_num):
                    nx, ny, nd, nc = board.get_next(x, y, direction)
                    if nc == "#":
                        break
                    else:
                        x, y, direction = nx, ny, nd

    return x, y, direction


class PseudoMatrix:

    data: dict
    x_range = []
    y_range = []

    def __init__(self, default_value=None):
        if default_value:
            self.data = defaultdict(lambda: defaultdict(lambda: default_value))
        else:
            self.data = defaultdict(lambda: dict)

        self.wrap_3d = False

    def do_wrap_3d(self):
        self.wrap_3d = True

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

    def get_next(self, curr_x, curr_y, direction):
        x, y = curr_x, curr_y
        while True:
            if direction == ">":
                x, y, direction = self._wrap(x + 1, y, direction)
            elif direction == "<":
                x, y, direction = self._wrap(x - 1, y, direction)
            elif direction == "^":
                x, y, direction = self._wrap(x, y - 1, direction)
            elif direction == "v":
                x, y, direction = self._wrap(x, y + 1, direction)
            else:
                raise Exception("Whoot?")

            if self[x, y] != " ":
                return x, y, direction, self[x, y]

    def _wrap(self, x, y, direction):
        if self.wrap_3d:
            # this is specific to my input
            # 1
            if x == 0 and 101 <= y <= 150 and direction == "<":
                return 51, 151 - y, ">"
            # 2
            if x == 50 and 1 <= y <= 50 and direction == "<":
                return 1, 151 - y, ">"
            # 3
            if x == 0 and 151 <= y <= 200 and direction == "<":
                return y - 100, 1, "v"
            # 4
            if 51 <= x <= 100 and y == 0 and direction == "^":
                return 1, x + 100, ">"
            # 5
            if x == 50 and 51 <= y <= 100 and direction == "<":
                return y - 50, 101, "v"
            # 6
            if 1 <= x <= 50 and y == 100 and direction == "^":
                return 51, x + 50, ">"
            # 7
            if x == 51 and 151 <= y <= 200 and direction == ">":
                return y - 100, 150, "^"
            # 8
            if 51 <= x <= 100 and y == 151 and direction == "v":
                return 50, x + 100, "<"
            # 9
            if 1 <= x <= 50 and y == 201 and direction == "v":
                return x + 100, 1, "v"
            # 10
            if 101 <= x <= 150 and y == 0 and direction == "^":
                return x - 100, 200, "^"
            # 11
            if x == 101 and 51 <= y <= 100 and direction == ">":
                return y + 50, 50, "^"
            # 12
            if 101 <= x <= 150 and y == 51 and direction == "v":
                return 100, x - 50, "<"
            # 13
            if x == 101 and 101 <= y <= 150 and direction == ">":
                return 150, 151 - y, "<"
            # 14
            if x == 151 and 1 <= y <= 50 and direction == ">":
                return 100, 151 - y, "<"
            return x, y, direction
        else:
            if x > self.x_range[1]:
                x = x - self.x_range[1] + self.x_range[0] - 1
            elif x < self.x_range[0]:
                x = x - self.x_range[0] + self.x_range[1] + 1

            if y > self.y_range[1]:
                y = y - self.y_range[1] + self.y_range[0] - 1
            elif y < self.y_range[0]:
                y = y - self.y_range[0] + self.y_range[1] + 1

            return x, y, direction


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
