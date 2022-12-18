import os
import time


def solve(puzzle_input):
    cubes = []
    for line in puzzle_input:
        cubes.append([int(c) for c in line.split(",")])

    exposed_sites = 0
    for cube in cubes:
        x = cube[0]
        y = cube[1]
        z = cube[2]
        if [x+1,y,z] not in cubes:
            exposed_sites += 1
        if [x-1,y,z] not in cubes:
            exposed_sites += 1
        if [x,y+1,z] not in cubes:
            exposed_sites += 1
        if [x,y-1,z] not in cubes:
            exposed_sites += 1
        if [x,y,z+1] not in cubes:
            exposed_sites += 1
        if [x,y,z-1] not in cubes:
            exposed_sites += 1

    print("Solution 1: {}".format(exposed_sites))

    exposed_sites = 0
    for cube in cubes:
        for neighbor in _neighbors(cube[0], cube[1], cube[2]):
            if neighbor not in cubes and _is_outside(neighbor, cubes):
                exposed_sites += 1

    print("Solution 2: {}".format(exposed_sites))


def _is_outside(air_cube, cubes):
    air_cubes = [air_cube]
    to_check = [air_cube]
    while to_check and len(air_cubes) <= len(cubes):
        curr_cube = to_check.pop()
        for neighbor in _neighbors(curr_cube[0], curr_cube[1], curr_cube[2]):
            if neighbor not in cubes and neighbor not in air_cubes:
                air_cubes.append(neighbor)
                to_check.append(neighbor)
    return len(air_cubes) >= len(cubes)


def _neighbors(x, y, z):
    return [[x+1,y,z], [x-1,y,z], [x,y+1,z], [x,y-1,z], [x,y,z+1], [x,y,z-1]]


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
