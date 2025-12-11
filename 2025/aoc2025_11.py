import os
import time

TEST_SOLUTION1 = 5
TEST_SOLUTION2 = 2


def solve(puzzle_input):
    connections = {}
    for line in puzzle_input:
        label, outputs = line.split(": ")
        connections[label] = outputs.split(" ")

    return count_paths(connections, "you"), count_paths2(connections)


def count_paths(connections, current_node):
    cnt = 0
    for next_node in connections[current_node]:
        if next_node == "out":
            cnt += 1
        else:
            cnt += count_paths(connections, next_node)
    return cnt


def count_paths2(connections):
    return count_paths3(connections, "svr", {})[3]

def count_paths3(connections, current_node, cache):
    cache_key = current_node
    if cache_key not in cache:
        num_paths_without = 0
        num_paths_with_dac = 0
        num_paths_with_fft = 0
        num_paths_with_both = 0

        for next_node in connections[current_node]:
            if next_node == "out":
                num_paths_without += 1
            else:
                sub_paths = count_paths3(connections, next_node, cache)
                num_paths_without += sub_paths[0]
                num_paths_with_dac += sub_paths[1]
                num_paths_with_fft += sub_paths[2]
                num_paths_with_both += sub_paths[3]

        if current_node == "dac":
            num_paths_with_dac += num_paths_without
            num_paths_without = 0
            num_paths_with_both += num_paths_with_fft
            num_paths_with_fft = 0
        elif current_node == "fft":
            num_paths_with_fft += num_paths_without
            num_paths_without = 0
            num_paths_with_both += num_paths_with_dac
            num_paths_with_dac = 0

        cache[cache_key] = [num_paths_without, num_paths_with_dac, num_paths_with_fft, num_paths_with_both]

    return cache[cache_key]

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
