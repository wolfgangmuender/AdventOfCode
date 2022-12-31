import os
import time

EMPTY = "|.......|"


def solve(puzzle_input):
    jet_pattern = list(puzzle_input[0])

    cave_heights = _fill_cave(jet_pattern, 2022)

    print("Solution 1: {}".format(sum(cave_heights)))

    cycle_length = 5 * len(jet_pattern)
    cycle_start = None

    cave_heights = _fill_cave(jet_pattern, 5 * cycle_length)

    while not cycle_start:
        if cycle_length > len(cave_heights):
            break

        for i in range(0, len(cave_heights)):
            if i + 2 * cycle_length == len(cave_heights):
                break
            if cave_heights[i] == cave_heights[i + cycle_length]:
                window_1 = cave_heights[i:i + cycle_length]
                window_2 = cave_heights[i + cycle_length:i + 2 * cycle_length]
                if window_1 == window_2:
                    cycle_start = i
                    break

        if not cycle_start:
            cycle_length += 5

    num_rocks = 1000000000000
    num_cycles = (num_rocks - cycle_start) // cycle_length
    remaining = (num_rocks - cycle_start) % cycle_length

    cycle_height = sum(cave_heights[cycle_start:cycle_start + cycle_length])

    print("Solution 2: {}".format(sum(cave_heights[0:cycle_start + remaining]) + num_cycles * cycle_height))


def _fill_cave(jet_pattern, max_num_rocks):
    cave = []
    cave_heights = []

    num_rocks = 0
    curr_jet_index = 0
    while num_rocks < max_num_rocks:
        old_height = len(cave)

        num_empty = cave.count(list(EMPTY))
        for i in range(0, 3 - num_empty):
            cave.append(list(EMPTY))

        rock_pos = len(cave)
        _append_rock(cave, num_rocks)

        go_on = True
        while go_on:
            curr_jet = jet_pattern[curr_jet_index]
            curr_jet_index = (curr_jet_index + 1) % len(jet_pattern)
            _shift(cave, curr_jet, rock_pos)
            go_on = _move_down(cave, rock_pos)
            rock_pos -= 1

        cave_heights.append(len(cave) - old_height)

        _settle(cave, rock_pos)

        num_rocks += 1

    return cave_heights


def _append_rock(cave, num_rocks):
    if num_rocks % 5 == 0:
        cave.append(list("|..@@@@.|"))
    elif num_rocks % 5 == 1:
        cave.append(list("|...@...|"))
        cave.append(list("|..@@@..|"))
        cave.append(list("|...@...|"))
    elif num_rocks % 5 == 2:
        cave.append(list("|..@@@..|"))
        cave.append(list("|....@..|"))
        cave.append(list("|....@..|"))
    elif num_rocks % 5 == 3:
        cave.append(list("|..@....|"))
        cave.append(list("|..@....|"))
        cave.append(list("|..@....|"))
        cave.append(list("|..@....|"))
    elif num_rocks % 5 == 4:
        cave.append(list("|..@@...|"))
        cave.append(list("|..@@...|"))
    else:
        raise Exception("Whoot?")


def _shift(cave, jet, rock_pos):
    for i in range(rock_pos, len(cave)):
        if jet == "<":
            for j in range(1, 8):
                if cave[i][j] == "@":
                    if cave[i][j - 1] != ".":
                        return
                    else:
                        break
        elif jet == ">":
            for j in range(7, 0, -1):
                if cave[i][j] == "@":
                    if cave[i][j + 1] != ".":
                        return
                    else:
                        break

    for i in range(rock_pos, len(cave)):
        if jet == "<":
            for j in range(1, 8):
                if cave[i][j] == "@":
                    cave[i][j - 1] = "@"
                    cave[i][j] = "."
        elif jet == ">":
            for j in range(7, 0, -1):
                if cave[i][j] == "@":
                    cave[i][j + 1] = "@"
                    cave[i][j] = "."


def _move_down(cave, rock_pos):
    if len(cave) == 1:
        return False

    for i in range(rock_pos, len(cave)):
        for j in range(1, 8):
            if cave[i][j] == "@" and cave[i - 1][j] not in (".", "@"):
                return False

    for i in range(rock_pos, len(cave)):
        for j in range(1, 8):
            if cave[i][j] == "@":
                cave[i - 1][j] = cave[i][j]
                cave[i][j] = "."

    if cave[-1] == list(EMPTY):
        cave.pop()

    return True


def _settle(cave, rock_pos):
    for i in range(rock_pos, len(cave)):
        for j in range(1, 8):
            if cave[i][j] == "@":
                cave[i][j] = "#"

    while len(cave) > 100:
        cave.pop(0)


def _print(cave):
    for i in range(0, len(cave)):
        print("".join(cave[-(1 + i)]))


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
