import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 7036
TEST_SOLUTION2 = 45

DIRECTIONS = {"^": [0, -1], "v": [0, 1], ">": [1, 0], "<": [-1, 0]}
TURNS = {"^": ["<", ">"], "v": ["<", ">"], ">": ["^", "v"], "<": ["^", "v"]}


def solve(puzzle_input):
    maze = PseudoMatrix()
    for line in puzzle_input:
        maze.append_row(line)

    xs, ys = maze.get_first_coordinate("S")

    start = tuple([xs, ys, ">"])
    visited = {start: 0}
    paths = {start: {start}}
    candidates = {start}
    candidate = None
    while candidates:
        candidate = get_next(candidates, visited)
        candidates.remove(candidate)
        x, y, d = candidate
        xd, yd = DIRECTIONS[d]

        if maze[x, y] == "E":
            break

        if maze[x + xd, y + yd] != "#":
            new_candidate = tuple([x + xd, y + yd, d])
            if new_candidate not in visited:
                visited[new_candidate] = visited[candidate] + 1
                paths[new_candidate] = paths[candidate] | {new_candidate}
                candidates.add(new_candidate)
            elif visited[new_candidate] == visited[candidate] + 1:
                paths[new_candidate].update(paths[candidate])

        for dn in TURNS[d]:
            new_candidate = tuple([x, y, dn])
            if new_candidate not in visited:
                visited[new_candidate] = visited[candidate] + 1000
                paths[new_candidate] = paths[candidate] | {new_candidate}
                candidates.add(new_candidate)
            elif visited[new_candidate] == visited[candidate] + 1000:
                paths[new_candidate].update(paths[candidate])

    return visited[candidate], len({tuple([p[0], p[1]]) for p in paths[candidate]})


def get_next(candidates, visited):
    the_candidate = None
    for candidate in candidates:
        if not the_candidate or visited[candidate] < visited[the_candidate]:
            the_candidate = candidate
    return the_candidate


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
