import os
import time
from itertools import combinations

TEST_SOLUTION1 = 21
TEST_SOLUTION2 = 525152


def solve(puzzle_input):
    rows = []
    rows2 = []
    for line in puzzle_input:
        records, damage_sizes_str = line.split(" ")
        damage_sizes = [int(n) for n in damage_sizes_str.split(",")]
        rows.append([records, damage_sizes])
        rows2.append([records + "?" + records + "?" + records + "?" + records + "?" + records, damage_sizes * 5])

    return sum(get_counts2(rows)), sum(get_counts2(rows2))


def get_counts(rows):
    counts = []
    for row in rows:
        records = [c for c in row[0]]
        damage_sizes = row[1]

        known_damages = len([r for r in records if r == "#"])
        unknown_records = len([r for r in records if r == "?"])
        total_damages = sum(damage_sizes)
        unknown_damages = total_damages - known_damages

        indices = [i for i, x in enumerate(records) if x == "?"]

        count = 0
        for comb in generate_combinations(unknown_records, unknown_damages):
            for index, new_value in zip(indices, comb):
                records[index] = new_value
            if cluster_sizes(records) == damage_sizes:
                count += 1
        counts.append(count)
    return counts


def generate_combinations(n, nhash):
    for positions in combinations(range(n), nhash):
        current_string = ['.' for _ in range(n)]
        for pos in positions:
            current_string[pos] = '#'
        yield ''.join(current_string)


def cluster_sizes(records):
    sizes = []
    curr = 0
    for r in records:
        if r == ".":
            if curr:
                sizes.append(curr)
            curr = 0
        else:
            curr += 1
    if curr:
        sizes.append(curr)
    return sizes


def get_counts2(rows):
    cache = {}
    counts = []
    for row in rows:
        curr = count_recursively(row[0], row[1], cache)
        counts.append(curr)
    return counts


def count_recursively(records, damage_sizes, cache):
    cache_key = records + "_" + "_".join([str(ds) for ds in damage_sizes])
    if cache_key in cache:
        return cache[cache_key]

    if not records:
        if damage_sizes:
            res = 0
        else:
            res = 1
    elif not damage_sizes:
        if "#" in records:
            res = 0
        else:
            res = 1
    elif records[0] == ".":
        res = count_recursively(records[1:], damage_sizes, cache)
    elif records[0] == "#":
        ds = damage_sizes[0]
        if len(records) < ds:
            res = 0
        elif "." in records[:ds]:
            res = 0
        elif len(records) > ds and "#" == records[ds]:
            res = 0
        elif len(records) == ds and len(damage_sizes) == 1:
            res = 1
        else:
            res = count_recursively(records[ds + 1:], damage_sizes[1:], cache)
    elif records[0] == "?":
        res1 = count_recursively("#" + records[1:], damage_sizes, cache)
        res2 = count_recursively("." + records[1:], damage_sizes, cache)
        res = res1 + res2
    else:
        raise Exception("Whoot?")

    cache[cache_key] = res

    return res


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
