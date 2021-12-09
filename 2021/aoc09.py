from functools import reduce

with open("input/input09.txt") as f:
    content = f.read().splitlines()

heights = []
for line in content:
    heights.append([int(height) for height in list(line)])

num_x = len(heights[0])
num_y = len(heights)

low_points = []
for y in range(0, num_y):
    for x in range(0, num_x):
        curr_height = heights[y][x]
        if y > 0 and heights[y - 1][x] <= curr_height:
            continue
        if y < num_y - 1 and heights[y + 1][x] <= curr_height:
            continue
        if x > 0 and heights[y][x - 1] <= curr_height:
            continue
        if x < num_x - 1 and heights[y][x + 1] <= curr_height:
            continue
        low_points.append({
            "x": x,
            "y": y,
            "height": curr_height,
        })

print("Solution 1: the sum of the risk levels of all low points on the heightmap is {}"
      .format(sum([low_point["height"] + 1 for low_point in low_points])))

for low_point in low_points:
    low_point["basin_size"] = 0

    visited_locations = []
    locations_to_explore = [[low_point["x"], low_point["y"]]]
    while len(locations_to_explore):
        x, y = locations_to_explore.pop(0)
        if [x, y] in visited_locations:
            continue

        visited_locations.append([x, y])
        if x < 0 or x >= num_x:
            continue
        if y < 0 or y >= num_y:
            continue
        if heights[y][x] == 9:
            continue

        low_point["basin_size"] += 1
        for diff in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            new_location = [x + diff[0], y + diff[1]]
            if new_location not in visited_locations:
                locations_to_explore.append(new_location)

basin_sizes = [low_point["basin_size"] for low_point in low_points]
basin_sizes.sort(reverse=True)

print("Solution 2: the product of the sizes of the three largest basins is {}"
      .format(reduce((lambda n, m: n * m), basin_sizes[0:3])))
