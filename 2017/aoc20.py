import os
import time
from copy import deepcopy
from operator import add

TEST_SOLUTION1 = 0
TEST_SOLUTION2 = 2


def solve(puzzle_input):
    particles = []
    for line in puzzle_input:
        p, v, a = line.split(", ")
        particles.append({
            "p": [int(i) for i in p[3:-1].split(",")],
            "v": [int(i) for i in v[3:-1].split(",")],
            "a": [int(i) for i in a[3:-1].split(",")],
        })

    min_a = None
    min_indexes = None
    for i in range(0, len(particles)):
        par = particles[i]
        val_a = manhattan(par["a"])
        if not min_a or val_a < min_a:
            min_a = val_a
            min_indexes = [i]
        elif val_a == min_a:
            min_indexes.append(i)

    ps = {i: deepcopy(particles[i]["p"]) for i in min_indexes}
    vs = {i: deepcopy(particles[i]["v"]) for i in min_indexes}
    all_v_growing = False
    while not all_v_growing:
        all_v_growing = True
        for i in min_indexes:
            vb = manhattan(vs[i])
            vs[i] = list(map(add, vs[i], particles[i]["a"]))
            ps[i] = list(map(add, ps[i], vs[i]))
            va = manhattan(vs[i])
            all_v_growing &= va > vb

    index_min = min(min_indexes, key=lambda i: manhattan(ps[i]))

    ps = {i: deepcopy(particles[i]["p"]) for i in range(0, len(particles))}
    vs = {i: deepcopy(particles[i]["v"]) for i in range(0, len(particles))}

    # considering the initial values of ps,vs,as it stands reasonable that after 1000 moves all particles move apart
    for _ in range(0, 1000):
        for i in ps.keys():
            vs[i] = list(map(add, vs[i], particles[i]["a"]))
            ps[i] = list(map(add, ps[i], vs[i]))

        to_remove = set()
        for i in ps.keys():
            for j in ps.keys():
                if i < j and ps[i] == ps[j]:
                    to_remove.add(i)
                    to_remove.add(j)

        for i in to_remove:
            del ps[i]
            del vs[i]

    return index_min, len(ps)


def manhattan(v):
    return sum([abs(v[i]) for i in range(0, len(v))])


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
