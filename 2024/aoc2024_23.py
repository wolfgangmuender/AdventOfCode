import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 7
TEST_SOLUTION2 = "co,de,ka,ta"


def solve(puzzle_input):
    connections = defaultdict(lambda: set())
    for line in puzzle_input:
        node1, node2 = line.split("-")
        connections[node1].add(node2)
        connections[node2].add(node1)

    triples = set()
    for node, conns in connections.items():
        for neighbor1 in conns:
            for neighbor2 in conns.intersection(connections[neighbor1]):
                triples.add(tuple(sorted([node, neighbor1, neighbor2])))

    largest_cluster = None
    for triple in triples:
        cluster = enlarge(triple, connections)
        cluster = tuple(sorted(cluster))
        largest_cluster = cluster if not largest_cluster or len(cluster) > len(largest_cluster) else largest_cluster

    return sum([1 if any(n.startswith("t") for n in triple) else 0 for triple in triples]), ','.join(map(str, largest_cluster))


def enlarge(triple, connections):
    cluster = {node for node in triple}
    for candidate in connections[triple[0]]:
        if cluster.issubset(connections[candidate]):
            cluster.add(candidate)
    return cluster


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
