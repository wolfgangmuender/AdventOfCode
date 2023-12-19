import os
import sys
import time
from copy import copy

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 102
TEST_SOLUTION2 = 94

DX = {"^": 0, "v": 0, ">": 1, "<": -1}
DY = {"^": -1, "v": 1, ">": 0, "<": 0}
REV = {".": ".", "^": "v", "v": "^", ">": "<", "<": ">"}


def solve(puzzle_input):
    heat_loss_map = PseudoMatrix()
    for line in puzzle_input:
        heat_loss_map.append_row([int(c) for c in line])

    return find_minimal_heat_loss(heat_loss_map, False), find_minimal_heat_loss(heat_loss_map, True)


def find_minimal_heat_loss(heat_loss_map, is_ultra_crucibles):
    start = {
        "x": 0,
        "y": 0,
        "dir": ".",
        "dir_count": 1,
        "heat_loss": 0
    }
    visited = {}
    queue = {get_key(start): start}
    while queue:
        curr = get_next(queue)
        if heat_loss_map.is_bottom_right(curr["x"], curr["y"]):
            return curr["heat_loss"]

        visited[get_key(curr)] = curr
        for neighbour in get_possible_neighbours(heat_loss_map, curr, is_ultra_crucibles):
            neighbour_key = get_key(neighbour)
            if neighbour_key not in visited:
                if neighbour_key in queue:
                    if neighbour["heat_loss"] < queue[neighbour_key]["heat_loss"]:
                        queue[neighbour_key] = neighbour
                else:
                    queue[neighbour_key] = neighbour

    return None


def get_key(node):
    return f"{node['x']}_{node['y']}_{node['dir']}_{node['dir_count']}"


def get_next(queue):
    the_next = min(queue.values(), key=lambda x: x['heat_loss'])
    queue.pop(get_key(the_next))
    return the_next


def get_possible_neighbours(heat_loss_map, curr, is_ultra_crucibles):
    possible_neighbours = []
    for d in ["^", "v", ">", "<"]:
        if d == REV[curr["dir"]]:
            continue
        max_direction = 10 if is_ultra_crucibles else 3
        if d == curr["dir"] and curr["dir_count"] == max_direction:
            continue
        if is_ultra_crucibles and curr["dir"] != "." and d != curr["dir"] and curr["dir_count"] < 4:
            continue

        x = curr["x"] + DX[d]
        y = curr["y"] + DY[d]
        if heat_loss_map.is_x_within(x) and heat_loss_map.is_y_within(y):
            possible_neighbours.append({
                "x": x,
                "y": y,
                "dir": d,
                "dir_count": curr["dir_count"] + 1 if d == curr["dir"] else 1,
                "heat_loss": curr["heat_loss"] + heat_loss_map[x, y]
            })
    return possible_neighbours


def find_path(heat_loss_map, curr_path, curr_directions, cache):
    if curr_path[-1][0] == heat_loss_map.x_range[1] and curr_path[-1][1] == heat_loss_map.y_range[1]:
        return heat_loss_map[curr_path[-1][0], curr_path[-1][1]]

    cache_key = get_cache_key(curr_path, curr_directions)
    if cache_key in cache:
        return cache[cache_key]

    heat_losses = []
    for d in ["^", "v", ">", "<"]:
        if d == REV[curr_directions[-1]]:
            continue
        x = curr_path[-1][0] + DX[d]
        y = curr_path[-1][1] + DY[d]
        cannot_go_on = len(curr_directions) >= 3 and len(set(curr_directions[-3:] + [d])) == 1
        if heat_loss_map.is_x_within(x) and heat_loss_map.is_y_within(y) and not cannot_go_on:
            curr_heat_loss = heat_loss_map[x, y] + find_path(heat_loss_map, copy(curr_path) + [[x, y]],
                                                             copy(curr_directions) + [d], cache)
            heat_losses.append(curr_heat_loss)

    cache[cache_key] = min(heat_losses)

    return cache[cache_key]


def get_cache_key(curr_path, curr_directions):
    cache_key = f"{curr_path[-1][0]}_{curr_path[-1][1]}_{curr_directions[-1]}"
    if len(curr_directions) >= 2:
        cache_key += f"_{curr_directions[-2]}"
    if len(curr_directions) >= 3:
        cache_key += f"_{curr_directions[-3]}"
    return cache_key


def get_min(total_heat_loss, start_points):
    min_val = 0
    min_ind = None
    for i in range(0, len(start_points)):
        x = start_points[i][0]
        y = start_points[i][1]
        if not min_val:
            min_val = total_heat_loss[x, y]
            min_ind = i
        elif total_heat_loss[x, y] < min_val:
            min_val = total_heat_loss[x, y]
            min_ind = i
    return start_points.pop(min_ind)


def get_nexts(heat_loss, visited, start_point, start_path):
    nexts = []
    for d in ["^", "v", ">", "<"]:
        x = start_point[0] + DX[d]
        y = start_point[1] + DY[d]
        cannot_go_on = len(start_path) >= 3 and len(set(start_path[-3:] + [d])) == 1
        if heat_loss.is_x_within(x) and heat_loss.is_y_within(y) and [x, y] not in visited and not cannot_go_on:
            nexts.append([[x, y], d])

    return nexts


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    test_input_file2 = test_input_file.replace(".txt", "-2.txt")
    if os.path.isfile(test_input_file):
        start = time.time()
        with open(test_input_file) as f:
            content1 = f.read().splitlines()
        if os.path.isfile(test_input_file2):
            with open(test_input_file2) as f:
                content2 = f.read().splitlines()
            solution1, _ = solve(content1)
            _, solution2 = solve(content2)
        else:
            solution1, solution2 = solve(content1)
        if solution1 != TEST_SOLUTION1:
            print(f"TEST solution 1 '{solution1}' not correct!")
            return
        if solution2 != TEST_SOLUTION2:
            print(f"TEST solution 2 '{solution2}' not correct!")
            return
        end = time.time()
        print_diff(end - start, True)
    else:
        open(test_input_file, 'a').close()

    input_file = "input/" + os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    if os.path.isfile(input_file):
        with open(input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
        print("Solution 1: {}".format(solution1))
        print("Solution 2: {}".format(solution2))
        end = time.time()
        print_diff(end - start, False)
    else:
        open(input_file, 'a').close()


def print_diff(diff, is_test):
    prefix = "TEST " if is_test else ""
    if diff >= 1:
        print("The {}solutions took {}s".format(prefix, round(diff)))
    else:
        print("The {}solutions took {}ms".format(prefix, round(diff * 1000)))


if __name__ == "__main__":
    main()
