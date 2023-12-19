from collections import defaultdict
from copy import deepcopy


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
            self.data = defaultdict(lambda: {})

    def __eq__(self, other):
        if self.x_range != other.x_range:
            return False
        if self.y_range != other.y_range:
            return False

        for x, y in self.iter():
            if self[x, y] != other[x, y]:
                return False

        return True

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

    def iter_x(self, direction=1):
        if direction == 1:
            for x in range(self.x_range[0], self.x_range[1] + 1):
                yield x
        else:
            for x in range(self.x_range[1], self.x_range[0] - 1, -1):
                yield x

    def iter_y(self, direction=1):
        if direction == 1:
            for y in range(self.y_range[0], self.y_range[1] + 1):
                yield y
        else:
            for y in range(self.y_range[1], self.y_range[0] - 1, -1):
                yield y

    def iter_columns(self):
        for x in self.iter_x():
            yield x, [self[x, y] for y in self.iter_y()]

    def iter_rows(self):
        for y in self.iter_y():
            yield y, [self[x, y] for x in self.iter_x()]

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

    def append_column(self, col):
        x = self.x_range[1] + 1 if self.x_range else 0
        y = self.y_range[0] if self.y_range else 0
        for elem in col:
            self[x, y] = elem
            y += 1

    def append_row(self, row):
        x = self.x_range[0] if self.x_range else 0
        y = self.y_range[1] + 1 if self.y_range else 0
        for elem in row:
            self[x, y] = elem
            x += 1

    def get_column(self, x):
        return [self[x, y] for y in self.iter_y()]

    def get_row(self, y):
        return [self[x, y] for x in self.iter_x()]

    def is_x_within(self, x):
        return self.x_range[0] <= x <= self.x_range[1]

    def is_y_within(self, y):
        return self.y_range[0] <= y <= self.y_range[1]

    def is_bottom_right(self, x, y):
        return x == self.x_range[1] and y == self.y_range[1]
