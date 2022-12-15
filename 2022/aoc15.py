import os
import time
from collections import defaultdict


def main(puzzle_input):
    cave_map = PseudoMatrix(".")
    sensors = []
    beacons = []
    for line in puzzle_input:
        sensor, beacon = line[10:].split(": closest beacon is at ")

        sensor_x, sensor_y = [int(val[2:]) for val in sensor.split(", ")]
        cave_map[sensor_x, sensor_y] = "S"
        sensors.append([sensor_x, sensor_y])

        beacon_x, beacon_y = [int(val[2:]) for val in beacon.split(", ")]
        cave_map[beacon_x, beacon_y] = "B"
        beacons.append([beacon_x, beacon_y])

    the_y = 2000000
    the_row = defaultdict(lambda: ".")
    for sensor, beacon in zip(sensors, beacons):
        if sensor[1] == the_y:
            the_row[sensor[0]] = "S"
        if beacon[1] == the_y:
            the_row[beacon[0]] = "B"

        dist = _dist(sensor, beacon)
        for diff_x in range(0, dist+1):
            if _dist(sensor, [sensor[0] + diff_x, the_y]) <= dist:
                if the_row[sensor[0] + diff_x] == ".":
                    the_row[sensor[0] + diff_x] = "#"
                if the_row[sensor[0] - diff_x] == ".":
                    the_row[sensor[0] - diff_x] = "#"

    taken_positions = len([val for val in the_row.values() if val in ["#", "S"]])

    print("Solution 1: {}".format(taken_positions))

    max_x = 4000000
    max_y = 4000000
    pos = [[0, max_x]] * (max_y+1)
    for sensor, beacon in zip(sensors, beacons):
        dist = _dist(sensor, beacon)
        for y in range(0, max_y+1):
            y_diff = abs(y-sensor[1])
            if y_diff <= dist:
                x_diff = dist - y_diff
                pos[y] = _cut(pos[y], [sensor[0] - x_diff, sensor[0] + x_diff])

    can_y = [y for y in range(0, max_y+1) if pos[y]]
    assert len(can_y) == 1
    y = can_y[0]
    assert len(pos[y]) == 2
    assert pos[y][0] == pos[y][1]
    x = pos[y][0]

    print("Solution 2: {}".format(x*4000000 + y))


def _dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def _cut(ranges, cut_off):
    new_ranges = []
    for i in range(0, len(ranges), 2):
        x1 = ranges[i]
        x2 = ranges[i+1]
        if cut_off[1] < x1:
            new_ranges.extend([x1, x2])
        elif cut_off[1] < x2:
            if cut_off[0] > x1:
                new_ranges.extend([x1, cut_off[0]-1])
            new_ranges.extend([cut_off[1]+1, x2])
        else:
            if cut_off[0] > x1 and cut_off[0] <= x2:
                new_ranges.extend([x1, cut_off[0]-1])
            elif cut_off[0] > x2:
                new_ranges.extend([x1, x2])

    return new_ranges


class PseudoMatrix:

    data: dict
    x_range = []
    y_range = []

    def __init__(self, default_value=None):
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

    def print(self):
        for y in self.iter_y():
            print(f"{y}".ljust(5) + "".join([self.data[x][y] for x in self.iter_x()]))


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
