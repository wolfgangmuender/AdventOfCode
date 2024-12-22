import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 1
TEST_SOLUTION2 = 285


def solve(puzzle_input):
    racetrack = PseudoMatrix("#")
    for line in puzzle_input:
        racetrack.append_row(line)

    time_to_save = 100 if len(puzzle_input) > 15 else 50

    xs, ys = racetrack.get_first_coordinate("S")
    xe, ye = racetrack.get_first_coordinate("E")
    forth = find_shortest_path(racetrack, xs, ys, xe, ye)
    back = find_shortest_path(racetrack, xe, ye, xs, ys)

    time_without_cheating = forth[tuple([xe, ye])]

    cheat_paths = find_shortest_paths_with_cheating(racetrack, xs, ys, back)
    num_cheat_paths = len([time_without_cheating - cp for cp in cheat_paths if time_without_cheating - cp >= time_to_save])

    extreme_cheat_paths = find_shortest_paths_with_extreme_cheating(racetrack, xs, ys, back)
    num_extreme_cheat_paths = len([time_without_cheating - cp for cp in extreme_cheat_paths if time_without_cheating - cp >= time_to_save])

    return num_cheat_paths, num_extreme_cheat_paths


def find_shortest_paths_with_cheating(racetrack, xs, ys, back):
    cheat_paths = []

    start = tuple([xs, ys])
    visited = {start: 0}
    candidates = {start}
    while candidates:
        candidate = get_next(candidates, visited)
        candidates.remove(candidate)
        x, y = candidate

        if racetrack[x, y] == "E":
            break

        for xd, yd in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            xn = x + xd
            yn = y + yd
            if racetrack[xn, yn] != "#":
                new_candidate = tuple([xn, yn])
                if new_candidate not in visited:
                    visited[new_candidate] = visited[candidate] + 1
                    candidates.add(new_candidate)
            else:
                xnn = x + 2 * xd
                ynn = y + 2 * yd
                if racetrack[xnn, ynn] == "E":
                    cheat_paths.append(visited[candidate] + 2)
                elif racetrack[xnn, ynn] != "#":
                    cheat_paths.append(visited[candidate] + 2 + back[tuple([xnn, ynn])])

    return cheat_paths


def find_shortest_paths_with_extreme_cheating(racetrack, xs, ys, back):
    cheat_paths = []
    cheatway = []

    start = tuple([xs, ys])
    visited = {start: 0}
    candidates = {start}
    while candidates:
        candidate = get_next(candidates, visited)
        candidates.remove(candidate)
        x, y = candidate

        if racetrack[x, y] == "E":
            break

        for xd, yd in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            xn = x + xd
            yn = y + yd
            if racetrack[xn, yn] != "#":
                new_candidate = tuple([xn, yn])
                if new_candidate not in visited:
                    visited[new_candidate] = visited[candidate] + 1
                    candidates.add(new_candidate)

        for xc, yc in racetrack.iter():
            cheat = abs(xc - x) + abs(yc - y)
            if 0 < cheat <= 20:
                if racetrack[xc, yc] == "E":
                    temp = visited[candidate] + cheat
                    cheat_paths.append(temp)
                    if temp == 12:
                        cheatway.append(tuple([y, x, yc, xc]))
                elif racetrack[xc, yc] != "#":
                    temp = visited[candidate] + cheat + back[tuple([xc, yc])]
                    cheat_paths.append(temp)
                    if temp == 12:
                        cheatway.append(tuple([y, x, yc, xc]))

    return cheat_paths


def find_shortest_path(racetrack, xs, ys, xe, ye):
    start = tuple([xs, ys])
    visited = {start: 0}
    candidates = {start}
    while candidates:
        candidate = get_next(candidates, visited)
        candidates.remove(candidate)
        x, y = candidate

        if [x, y] == [xe, ye]:
            break

        for xn, yn in racetrack.iter_direct_neighbours(x, y):
            if racetrack[xn, yn] != "#":
                new_candidate = tuple([xn, yn])
                if new_candidate not in visited:
                    visited[new_candidate] = visited[candidate] + 1
                    candidates.add(new_candidate)

    return visited


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
