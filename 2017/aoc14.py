import os
import time
from collections import defaultdict
from copy import deepcopy
from math import floor

TEST_SOLUTION1 = 8108
TEST_SOLUTION2 = 1242


def solve(puzzle_input):
    key_string = puzzle_input[0]

    grid = PseudoMatrix(0)
    num_used = 0
    for i in range(0, 128):
        knot_hash = get_knot_hash(f"{key_string}-{i}")
        bits = []
        for c in knot_hash:
            bits += hex_to_bits(c)
        grid.append_row(bits)
        num_used += bits.count(1)

    num_groups = 0
    visited = []
    for x, y in grid.iter():
        if grid[x, y] == 1 and [x, y] not in visited:
            visited.extend(collect_group(grid, x, y))
            num_groups += 1
        else:
            visited.append([x, y])

    return num_used, num_groups


def get_knot_hash(input_string):
    lengths = [ord(c) for c in input_string]
    lengths.extend([17, 31, 73, 47, 23])

    sparse_hash = list(range(0, 256))

    curr = 0
    skip_size = 0
    for _ in range(0, 64):
        curr, skip_size = apply_lengths(sparse_hash, lengths, curr, skip_size)

    dense_hash = []
    for i in range(0, 16):
        dense_hash.append(sparse_hash[i * 16])
        for j in range(1, 16):
            dense_hash[i] ^= sparse_hash[i * 16 + j]

    knot_hash = "".join([hex(dh)[2:].rjust(2, "0") for dh in dense_hash])

    return knot_hash


def apply_lengths(numbers, lengths, curr, skip_size):
    num_numbers = len(numbers)
    for length in lengths:
        for i in range(0, floor(length / 2)):
            source_index = (curr + i) % num_numbers
            target_index = (curr + length - 1 - i) % num_numbers

            source = numbers[source_index]
            target = numbers[target_index]

            numbers[target_index] = source
            numbers[source_index] = target

        curr = (curr + length + skip_size) % num_numbers
        skip_size += 1
    return curr, skip_size


def hex_to_bits(the_hex):
    return [int(b) for b in bin(int(the_hex, 16))[2:].zfill(4)]


def collect_group(grid, x0, y0):
    visited = []
    to_check = [[x0, y0]]
    while to_check:
        x, y = to_check.pop()
        visited.append([x, y])

        for nb in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]:
            if grid[nb[0], nb[1]] == 1 and nb not in to_check and nb not in visited:
                to_check.append(nb)

    return visited


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
