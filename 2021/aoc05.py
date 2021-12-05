from collections import defaultdict

with open("input/input05.txt") as f:
    content = f.read().splitlines()


class Vent:

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def is_horizontal(self):
        return self.x1 == self.x2

    def is_vertical(self):
        return self.y1 == self.y2

    def x_range(self):
        if self.x1 <= self.x2:
            return range(self.x1, self.x2 + 1)
        else:
            return range(self.x1, self.x2 - 1, -1)

    def y_range(self):
        if self.y1 <= self.y2:
            return range(self.y1, self.y2 + 1)
        else:
            return range(self.y1, self.y2 - 1, -1)

    def __str__(self):
        return "{},{} -> {},{}".format(self.x1, self.y1, self.x2, self.y2)


vents = []
for line in content:
    line_split = line.split(' -> ')
    start = line_split[0].split(',')
    end = line_split[1].split(',')
    vents.append(Vent(int(start[0]), int(start[1]), int(end[0]), int(end[1])))

positions1 = defaultdict(lambda: defaultdict(lambda: 0))
positions2 = defaultdict(lambda: defaultdict(lambda: 0))
for vent in vents:
    if vent.is_horizontal():
        for y in vent.y_range():
            positions1[vent.x1][y] += 1
            positions2[vent.x1][y] += 1
    elif vent.is_vertical():
        for x in vent.x_range():
            positions1[x][vent.y1] += 1
            positions2[x][vent.y1] += 1
    else:
        for x, y in zip(vent.x_range(), vent.y_range()):
            positions2[x][y] += 1

num_overlaps1 = 0
for x in positions1.keys():
    for y in positions1[x].keys():
        if positions1[x][y] > 1:
            num_overlaps1 += 1

num_overlaps2 = 0
for x in positions2.keys():
    for y in positions2[x].keys():
        if positions2[x][y] > 1:
            num_overlaps2 += 1

print("Solution 1: on {} points do at least two lines overlap".format(num_overlaps1))
print("Solution 2: on {} points do at least two lines overlap".format(num_overlaps2))
