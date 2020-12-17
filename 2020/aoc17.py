from collections import defaultdict
from copy import deepcopy

with open("input/input17.txt") as f:
    content = f.read().splitlines()


def count_active_cubes(current_cube_grid, curr_w_range, curr_z_range, curr_y_range, curr_x_range):
    active_cubes = 0
    for curr_w in curr_w_range:
        for curr_z in curr_z_range:
            for curr_y in curr_y_range:
                row = [current_cube_grid[curr_w][curr_z][curr_y][curr_x] for curr_x in curr_x_range]
                active_cubes += row.count('#')
    return active_cubes


def count_adjacent_active_cubes(current_cube_grid, the_w, the_z, the_y, the_x):
    active_cubes = 0
    for diff_w in w_neighbours:
        curr_w = the_w + diff_w
        for diff_z in [-1, 0, 1]:
            curr_z = the_z + diff_z
            for diff_y in [-1, 0, 1]:
                curr_y = the_y + diff_y
                for diff_x in [-1, 0, 1]:
                    if 0 == diff_w == diff_z == diff_y == diff_x:
                        continue
                    curr_x = the_x + diff_x
                    active_cubes += 1 if current_cube_grid[curr_w][curr_z][curr_y][curr_x] == '#' else 0
    return active_cubes


initial_cube_grid = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: '.'))))
initial_w = 0
initial_z = 0
initial_y = 0
initial_x = 0
for line in content:
    initial_x = 0
    for char in line:
        if char == '#':
            initial_cube_grid[initial_w][initial_z][initial_y][initial_x] = '#'
        initial_x += 1
    initial_y += 1

initial_y_range = list(range(0, initial_y))
initial_x_range = list(range(0, initial_x))
total_active_cubes = count_active_cubes(initial_cube_grid, [0], [0], initial_y_range, initial_x_range)

w_neighbours = [0]

next_grid = deepcopy(initial_cube_grid)
w_range = [0]
z_range = [0]
y_range = initial_y_range
x_range = initial_x_range
for i in range(1, 7):
    curr_grid = next_grid
    next_grid = deepcopy(curr_grid)
    z_range = [z_range[0] - 1] + z_range + [z_range[-1] + 1]
    y_range = [y_range[0] - 1] + y_range + [y_range[-1] + 1]
    x_range = [x_range[0] - 1] + x_range + [x_range[-1] + 1]
    w = 0
    for z in z_range:
        for y in y_range:
            for x in x_range:
                active_adjacent_cubes = count_adjacent_active_cubes(curr_grid, 0, z, y, x)
                if curr_grid[w][z][y][x] == '#':
                    next_grid[w][z][y][x] = '#' if active_adjacent_cubes in [2, 3] else '.'
                if curr_grid[w][z][y][x] == '.':
                    next_grid[w][z][y][x] = '#' if active_adjacent_cubes == 3 else '.'
    total_active_cubes = count_active_cubes(next_grid, w_range, z_range, y_range, x_range)

print("Solution 1: after the sixth cycle {} active cubes are left".format(total_active_cubes))

w_neighbours = [-1, 0, 1]

next_grid = deepcopy(initial_cube_grid)
w_range = [0]
z_range = [0]
y_range = initial_y_range
x_range = initial_x_range
for i in range(1, 7):
    curr_grid = next_grid
    next_grid = deepcopy(curr_grid)
    w_range = [w_range[0] - 1] + w_range + [w_range[-1] + 1]
    z_range = [z_range[0] - 1] + z_range + [z_range[-1] + 1]
    y_range = [y_range[0] - 1] + y_range + [y_range[-1] + 1]
    x_range = [x_range[0] - 1] + x_range + [x_range[-1] + 1]
    for w in w_range:
        for z in z_range:
            for y in y_range:
                for x in x_range:
                    active_adjacent_cubes = count_adjacent_active_cubes(curr_grid, w, z, y, x)
                    if curr_grid[w][z][y][x] == '#':
                        next_grid[w][z][y][x] = '#' if active_adjacent_cubes in [2, 3] else '.'
                    if curr_grid[w][z][y][x] == '.':
                        next_grid[w][z][y][x] = '#' if active_adjacent_cubes == 3 else '.'
    total_active_cubes = count_active_cubes(next_grid, w_range, z_range, y_range, x_range)

print("Solution 2: after the sixth cycle {} active cubes are left".format(total_active_cubes))
