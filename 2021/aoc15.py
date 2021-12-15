import os
import time


def main(puzzle_input):
    risks = []
    for line in puzzle_input:
        risks.append([int(r) for r in line])
    size = len(risks)

    risk_map1 = get_risk_map(risks, size)

    print("Solution 1: the lowest total risk of any path from the top left to the bottom right is {}"
          .format(risk_map1[key([size - 1, size - 1])]))

    risks2 = enlarge_risks(risks, size)
    size2 = len(risks2)
    risk_map2 = get_risk_map(risks2, size2)

    print("Solution 2: the lowest total risk of any path from the top left to the bottom right is {}"
          .format(risk_map2[key([size2 - 1, size2 - 1])]))


def get_risk_map(risks, size):
    risk_map = {}
    unvisited_points_with_risk = set()
    visited_points = []

    risk_map[key([0, 0])] = 0
    unvisited_points_with_risk.add(key([0, 0]))

    while unvisited_points_with_risk:
        up = get_unvisited_point_with_minimal_risk(unvisited_points_with_risk, risk_map)
        upr = risk_map[up]

        unvisited_points_with_risk.remove(up)
        visited_points.append(up)

        for neighbour in get_neighbours(up, size):
            nk = key(neighbour)
            if nk not in visited_points:
                combined_risk = upr + risks[neighbour[0]][neighbour[1]]
                risk_map[nk] = combined_risk if nk not in risk_map else min(risk_map[nk], combined_risk)
                unvisited_points_with_risk.add(nk)

    return risk_map


def key(point):
    return "{}_{}".format(point[0], point[1])


def get_unvisited_point_with_minimal_risk(unvisited_points_with_risk, risk_map):
    unvisited_point_with_minimal_risk = None
    for up in unvisited_points_with_risk:
        if not unvisited_point_with_minimal_risk:
            unvisited_point_with_minimal_risk = up
        elif risk_map[up] < risk_map[unvisited_point_with_minimal_risk]:
            unvisited_point_with_minimal_risk = up
    return unvisited_point_with_minimal_risk


def get_neighbours(point, size):
    i, j = [int(p) for p in point.split("_")]

    neighbours = []
    if i > 0:
        neighbours.append([i - 1, j])
    if i < size - 1:
        neighbours.append([i + 1, j])
    if j > 0:
        neighbours.append([i, j - 1])
    if j < size - 1:
        neighbours.append([i, j + 1])

    return neighbours


def enlarge_risks(risks, size):
    new_risks = []
    for i in range(0, 5):
        new_risks.append([])
        for j in range(0, 5):
            new_risks[i].append(copy_risks(risks, i + j))

    enlarged_risks = []
    for i in range(0, 5):
        for n in range(0, size):
            enlarged_risks.append([])
            for j in range(0, 5):
                enlarged_risks[-1] += new_risks[i][j][n]

    return enlarged_risks


def copy_risks(risks, offset):
    new_risks = []
    for line in risks:
        new_risks.append([map_risk(risk, offset) for risk in line])
    return new_risks


def map_risk(risk, offset):
    new_risk = risk + offset
    return new_risk if new_risk < 10 else new_risk - 9


if __name__ == "__main__":
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    main(content)
    end = time.time()
    print("The solutions took {} seconds".format(end - start))
