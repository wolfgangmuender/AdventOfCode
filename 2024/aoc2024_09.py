import os
import time
from copy import copy, deepcopy

TEST_SOLUTION1 = 1928
TEST_SOLUTION2 = 2858


def solve(puzzle_input):
    blocks = []
    block_map = []
    id_sequence = 0
    is_file = True
    for n in puzzle_input[0]:
        if is_file:
            block_map.append({"length": int(n), "value": id_sequence})
            blocks += int(n) * [id_sequence]
            id_sequence += 1
        else:
            block_map.append({"length": int(n), "value": -1})
            blocks += int(n) * [-1]
        is_file = not is_file

    blocks_reordered = copy(blocks)
    while -1 in blocks_reordered:
        n = blocks_reordered.pop()
        blocks_reordered[blocks_reordered.index(-1)] = n

    filesystem_checksum1 = sum([i * blocks_reordered[i] for i in range(0, len(blocks_reordered))])

    blocks_map_curr = deepcopy(block_map)
    block_map_reordered = []
    while len(blocks_map_curr):
        curr = blocks_map_curr.pop()
        if curr["length"] == 0:
            continue
        if curr["value"] == -1:
            block_map_reordered.insert(0, curr)
        else:
            new_index = find_new_index(blocks_map_curr, curr)
            if new_index is False:
                block_map_reordered.insert(0, curr)
            else:
                blocks_map_curr[new_index]["length"] -= curr["length"]
                blocks_map_curr.insert(new_index, curr)
                block_map_reordered.insert(0, {"length": curr["length"], "value": -1})

    filesystem_checksum2 = 0
    curr_index = 0
    for block in block_map_reordered:
        for i in range(0, block["length"]):
            if block["value"] != -1:
                filesystem_checksum2 += curr_index * block["value"]
            curr_index += 1

    return filesystem_checksum1, filesystem_checksum2


def find_new_index(blocks_map, curr):
    for i in range(0, len(blocks_map)):
        if blocks_map[i]["value"] == -1 and blocks_map[i]["length"] >= curr["length"]:
            return i
    return False


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
