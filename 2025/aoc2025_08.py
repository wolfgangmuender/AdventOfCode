import math
import os
import time
from itertools import islice

TEST_SOLUTION1 = 40
TEST_SOLUTION2 = 25272


def solve(puzzle_input):
    positions = []
    for line in puzzle_input:
        positions.append(tuple([int(c) for c in line.split(",")]))

    distances = {}
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            pos1 = positions[i]
            pos2 = positions[j]
            dist = math.dist(pos1, pos2)
            distances[(pos1, pos2)] = dist

    num_iterations = 1000 if len(positions) == 1000 else 10

    num_iter = 0
    solution1 = 0
    solution2 = 0
    clusters = []
    for (pos1, pos2), dist in islice(sorted(distances.items(), key=lambda x: x[1]), len(positions) * len(positions)):
        num_iter += 1

        ind1 = [i for i in range(len(clusters)) if pos1 in clusters[i]]
        ind2 = [i for i in range(len(clusters)) if pos2 in clusters[i]]
        if ind1 and ind2:
            if ind1[0] != ind2[0]:
                clusters[ind1[0]].update(clusters[ind2[0]])
                clusters.pop(ind2[0])
        elif ind1:
            clusters[ind1[0]].add(pos1)
            clusters[ind1[0]].add(pos2)
        elif ind2:
            clusters[ind2[0]].add(pos1)
            clusters[ind2[0]].add(pos2)
        else:
            clusters.append({pos1, pos2})

        if num_iter == num_iterations:
            sorted_clusters = sorted(clusters, key=len, reverse=True)
            solution1 = math.prod([len(c) for c in sorted_clusters[:3]])

        if len(clusters) == 1 and len(clusters[0]) == len(positions):
            solution2 = pos1[0] * pos2[0]
            break

    return solution1, solution2


def intersects_at(clusters, cluster):
    for i in range(len(clusters)):
        existing_cluster = clusters[i]
        if not existing_cluster.isdisjoint(cluster):
            return i
    return None


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
