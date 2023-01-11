import os
import time
from math import floor

from utils import input_to_int_list

TEST_SOLUTION1 = 12
TEST_SOLUTION2 = "3efbe78a8d82f29979031a4aa0b16a9d"


def solve(puzzle_input):
    lengths1 = input_to_int_list(puzzle_input[0], ",")
    if len(lengths1) == 4:
        # test input special handling
        lengths2 = [ord(c) for c in "1,2,3"]
        lengths2.extend([17, 31, 73, 47, 23])
    else:
        lengths2 = [ord(c) for c in puzzle_input[0]]
        lengths2.extend([17, 31, 73, 47, 23])

    if len(lengths1) == 4:
        # test input special handling
        sparse_hash = list(range(0, 5))
    else:
        sparse_hash = list(range(0, 256))

    apply_lengths(sparse_hash, lengths1, 0, 0)

    solution1 = sparse_hash[0] * sparse_hash[1]

    sparse_hash = list(range(0, 256))
    curr = 0
    skip_size = 0
    for _ in range(0, 64):
        curr, skip_size = apply_lengths(sparse_hash, lengths2, curr, skip_size)

    dense_hash = []
    for i in range(0, 16):
        dense_hash.append(sparse_hash[i*16])
        for j in range(1, 16):
            dense_hash[i] ^= sparse_hash[i*16 + j]

    knot_hash = "".join([hex(dh)[2:].rjust(2, "0") for dh in dense_hash])

    return solution1, knot_hash


def apply_lengths(numbers, lengths, curr, skip_size):
    num_numbers = len(numbers)
    for length in lengths:
        for i in range(0, floor(length/2)):
            source_index = (curr + i) % num_numbers
            target_index = (curr + length - 1 - i) % num_numbers

            source = numbers[source_index]
            target = numbers[target_index]

            numbers[target_index] = source
            numbers[source_index] = target

        curr = (curr + length + skip_size) % num_numbers
        skip_size += 1
    return curr, skip_size


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
