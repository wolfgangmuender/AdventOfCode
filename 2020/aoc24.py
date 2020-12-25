from collections import defaultdict
from copy import copy, deepcopy

with open("input/input24.txt") as f:
    content = f.read().splitlines()


def separated_string_to_list_of_int(the_string, separator):
    return list(map(lambda x: int(x), the_string.split(separator)))


steps = []
for line in content:
    curr_steps = []
    curr_line = copy(line)
    while curr_line:
        if curr_line.startswith('e') or curr_line.startswith('w'):
            curr_steps.append(curr_line[0:1])
            curr_line = curr_line[1:]
        elif curr_line.startswith('s') or curr_line.startswith('n'):
            curr_steps.append(curr_line[0:2])
            curr_line = curr_line[2:]
        else:
            raise Exception
    steps.append(curr_steps)


def get_coordinate_string(the_coordinates):
    return str(the_coordinates[0]) + "," + str(the_coordinates[1])


def get_adjacent(the_coordinates, the_step):
    adjacent_coordinates = copy(the_coordinates)
    if the_step == 'e':
        adjacent_coordinates[0] += 1
    elif the_step == 'ne':
        adjacent_coordinates[0] += 1
        adjacent_coordinates[1] += 1
    elif the_step == 'se':
        adjacent_coordinates[1] -= 1
    elif the_step == 'w':
        adjacent_coordinates[0] -= 1
    elif the_step == 'nw':
        adjacent_coordinates[1] += 1
    elif the_step == 'sw':
        adjacent_coordinates[0] -= 1
        adjacent_coordinates[1] -= 1
    else:
        raise Exception

    return adjacent_coordinates


tiles = defaultdict(lambda: -1)
for curr_steps in steps:
    coordinates = [0, 0]
    for curr_step in curr_steps:
        coordinates = get_adjacent(coordinates, curr_step)
    tiles[get_coordinate_string(coordinates)] *= -1

print("Solution 1: there are {} tiles with the black side up".format(
    sum([1 for coordinate_string in tiles.keys() if tiles[coordinate_string] == 1])))

next_tiles = deepcopy(tiles)
for i in range(0, 100):
    curr_tiles = next_tiles
    next_tiles = deepcopy(curr_tiles)

    number_of_black_adjacent = defaultdict(lambda: 0)

    for coordinate_string, color in curr_tiles.items():
        if color == 1:
            coordinates = separated_string_to_list_of_int(coordinate_string, ',')
            black_adjacent_count = 0
            for direction in ['e', 'ne', 'se', 'w', 'nw', 'sw']:
                adjacent_coordinates = get_adjacent(coordinates, direction)
                adjacent_coordinate_string = get_coordinate_string(adjacent_coordinates)
                number_of_black_adjacent[adjacent_coordinate_string] += 1
                if adjacent_coordinate_string in curr_tiles and curr_tiles[adjacent_coordinate_string] == 1:
                    black_adjacent_count += 1
            if black_adjacent_count == 0 or black_adjacent_count > 2:
                next_tiles[coordinate_string] = -1

    for coordinate_string, black_adjacent_count in number_of_black_adjacent.items():
        if curr_tiles[coordinate_string] == -1 and black_adjacent_count == 2:
            next_tiles[coordinate_string] = 1

print("Solution 2: after 100 days there are {} tiles with the black side up".format(
    sum([1 for coordinate_string in next_tiles.keys() if next_tiles[coordinate_string] == 1])))
