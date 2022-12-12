import os
import time


ABC = "abcdefghijklmnopqrstuvwxyz"


def main(puzzle_input):
    heightmap = {}
    start_point = None
    stop_point = None

    x = 0
    y = 0
    for line in puzzle_input:
        x = 0
        for c in line:
            curr_point = key([x, y])
            if c == "S":
                heightmap[curr_point] = 0
                start_point = curr_point
            elif c == "E":
                heightmap[curr_point] = len(ABC)-1
                stop_point = curr_point
            else:
                heightmap[curr_point] = ABC.index(c)
            x += 1
        y += 1

    max_x = x-1
    max_y = y-1

    fewest_steps = get_fewest_steps_map(heightmap, max_x, max_y, start_point)[stop_point]
    print("Solution 1: {}".format(fewest_steps))

    minimal_fewest_steps = fewest_steps
    for start_point in heightmap.keys():
        if heightmap[start_point] == 0:
            fewest_steps_map = get_fewest_steps_map(heightmap, max_x, max_y, start_point)
            if stop_point in fewest_steps_map and fewest_steps_map[stop_point] < minimal_fewest_steps:
                minimal_fewest_steps = fewest_steps_map[stop_point]

    print("Solution 2: {}".format(minimal_fewest_steps))


def get_fewest_steps_map(heightmap, max_x, max_y, start_point):
    fewest_steps_map = {}
    unvisited_points = set()
    visited_points = []

    fewest_steps_map[start_point] = heightmap[start_point]
    unvisited_points.add(start_point)

    while unvisited_points:
        curr_point = get_next(unvisited_points, fewest_steps_map)

        unvisited_points.remove(curr_point)
        visited_points.append(curr_point)

        for neighbour in get_neighbours(curr_point, max_x, max_y):
            if neighbour not in visited_points and heightmap[neighbour] <= heightmap[curr_point] + 1:
                fewest_steps_map[neighbour] = fewest_steps_map[curr_point] + 1
                unvisited_points.add(neighbour)

    return fewest_steps_map


def get_next(unvisited_points, potential_map):
    next_point = None
    for unvisited_point in unvisited_points:
        if not next_point:
            next_point = unvisited_point
        elif potential_map[unvisited_point] < potential_map[next_point]:
            next_point = unvisited_point
    return next_point


def get_neighbours(point, max_x, max_y):
    x, y = [int(p) for p in point.split("_")]

    neighbours = []
    if x > 0:
        neighbours.append(key([x - 1, y]))
    if x < max_x:
        neighbours.append(key([x + 1, y]))
    if y > 0:
        neighbours.append(key([x, y - 1]))
    if y < max_y:
        neighbours.append(key([x, y + 1]))

    return neighbours


def key(coordinates):
    return "{}_{}".format(coordinates[0], coordinates[1])


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
