import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 6
TEST_SOLUTION2 = 2


def solve(puzzle_input):
    program_connections = defaultdict(lambda: set())
    for line in puzzle_input:
        program, connections_string = line.split(" <-> ")
        connections = connections_string.split(", ")

        program_connections[program].update(connections)
        for connection in connections:
            program_connections[connection].add(program)

    groups = {}
    start_programs = sorted(program_connections.keys())
    while start_programs:
        start_program = start_programs.pop(0)
        print(start_program)
        groups[start_program] = collect_group_members(program_connections, start_program)
        start_programs = [sp for sp in start_programs if sp not in groups[start_program]]

    return len(groups["0"]), len(groups)


def collect_group_members(program_connections, start_program):
    group_members = set()
    to_visit = [start_program]
    while to_visit:
        curr = to_visit.pop()
        group_members.add(curr)
        for connection in program_connections[curr]:
            if connection not in group_members:
                to_visit.append(connection)

    return group_members


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    if os.path.isfile(test_input_file):
        with open(test_input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
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
