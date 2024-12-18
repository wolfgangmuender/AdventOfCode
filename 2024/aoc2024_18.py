import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 22
TEST_SOLUTION2 = "6,1"


def solve(puzzle_input):
    positions = []
    for line in puzzle_input:
        positions.append(([int(n) for n in line.split(",")]))

    dim = 70 if len(positions) > 25 else 6
    num = 1024 if len(positions) > 25 else 12
    end = tuple([dim, dim])

    visited0 = None

    is_open = True
    while is_open:
        visited = find_shortest_path(dim, positions, num)
        if not visited0:
            visited0 = visited

        if end in visited:
            num += 1
        else:
            is_open = False

    return visited0[end], f"{positions[num - 1][0]},{positions[num - 1][1]}"


def find_shortest_path(dim, positions, num):
    initial_map = PseudoMatrix(".")
    initial_map[0, 0] = "."
    initial_map[dim, dim] = "."
    for position in positions[:num]:
        x, y = position
        initial_map[x, y] = "#"

    start = tuple([0, 0])
    visited = {start: 0}
    candidates = {start}
    while candidates:
        candidate = get_next(candidates, visited)
        candidates.remove(candidate)
        x, y = candidate
        for xn, yn in initial_map.iter_direct_neighbours(x, y):
            new_candidate = tuple([xn, yn])
            if initial_map[new_candidate[0], new_candidate[1]] != "#" and new_candidate not in visited:
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
