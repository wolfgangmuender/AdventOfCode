from collections import defaultdict

with open("input/input12.txt") as f:
    content = f.read().splitlines()

connections = defaultdict(set)
for line in content:
    cave1, cave2 = line.split("-")
    connections[cave1].add(cave2)
    connections[cave2].add(cave1)


class Path():

    def __init__(self, path, special_small_cave):
        self.path = path
        self.special_small_cave = special_small_cave

    def curr_cave(self):
        return self.path[-1]

    def clone(self):
        return Path(self.path.copy(), self.special_small_cave)

    def can_be_added1(self, next_cave):
        return next_cave.isupper() or next_cave not in self.path

    def can_be_added2(self, next_cave):
        if next_cave.isupper() or next_cave not in self.path:
            return True
        if next_cave == "start":
            return False
        if self.special_small_cave:
            return False
        else:
            self.special_small_cave = next_cave
            return True

    def add(self, next_cave):
        self.path.append(next_cave)


paths = []
open_paths = [Path(["start"], None)]
while open_paths:
    curr_path = open_paths.pop()
    curr_connections = connections[curr_path.curr_cave()]
    for curr_connection in curr_connections:
        new_path = curr_path.clone()
        if new_path.can_be_added1(curr_connection):
            new_path.add(curr_connection)
            if curr_connection == "end":
                paths.append(new_path)
            else:
                open_paths.append(new_path)

print("Solution 1: there are {} paths through this cave system that visit small caves at most once".format(len(paths)))

paths = []
open_paths = [Path(["start"], None)]
while open_paths:
    curr_path = open_paths.pop()
    curr_connections = connections[curr_path.curr_cave()]
    for curr_connection in curr_connections:
        new_path = curr_path.clone()
        if new_path.can_be_added2(curr_connection):
            new_path.add(curr_connection)
            if curr_connection == "end":
                paths.append(new_path)
            else:
                open_paths.append(new_path)

print("Solution 2: there are {} paths through this cave system that visit small caves at most once".format(len(paths)))
