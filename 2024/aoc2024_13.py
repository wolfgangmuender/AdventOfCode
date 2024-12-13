import os
import time

TEST_SOLUTION1 = 480
TEST_SOLUTION2 = 875318608908


def solve(puzzle_input):
    machines = []
    machine = None
    for line in puzzle_input:
        if not machine or not line:
            machine = {
                "A": None,
                "B": None,
                "P": None,
            }
        if line.startswith("Button A"):
            x, y = [int(n) for n in line.replace("Button A: X+", "").replace("Y+", "").split(", ")]
            machine["A"] = [x, y]
        elif line.startswith("Button B"):
            x, y = [int(n) for n in line.replace("Button B: X+", "").replace("Y+", "").split(", ")]
            machine["B"] = [x, y]
        elif line.startswith("Prize"):
            x, y = [int(n) for n in line.replace("Prize: X=", "").replace("Y=", "").split(", ")]
            machine["P"] = [x, y]
            machines.append(machine)

    total_coins1 = 0
    total_coins2 = 0
    for machine in machines:
        num_a, num_b = get_moves(machine["A"][0], machine["A"][1], machine["B"][0], machine["B"][1], machine["P"][0], machine["P"][1])
        if is_valid_solution(machine["A"][0], machine["A"][1], machine["B"][0], machine["B"][1], machine["P"][0], machine["P"][1], num_a, num_b):
            num_a = round(num_a)
            num_b = round(num_b)
            if 0 < num_a < 100 and 0 < num_b < 100:
                coins = 3 * num_a + num_b
                total_coins1 += coins

        num_a, num_b = get_moves(machine["A"][0], machine["A"][1], machine["B"][0], machine["B"][1], machine["P"][0] + 10000000000000, machine["P"][1] + 10000000000000)
        if is_valid_solution(machine["A"][0], machine["A"][1], machine["B"][0], machine["B"][1], machine["P"][0] + 10000000000000, machine["P"][1] + 10000000000000, num_a, num_b):
            num_a = round(num_a)
            num_b = round(num_b)
            coins = 3 * num_a + num_b
            total_coins2 += coins

    return total_coins1, total_coins2


def get_moves(xa, ya, xb, yb, xp, yp):
    num_b = (yp - ya * xp / xa) / (yb - ya * xb / xa)
    num_a = (xp - num_b * xb) / xa
    return num_a, num_b


def is_valid_solution(xa, ya, xb, yb, xp, yp, num_a, num_b):
    num_a = round(num_a)
    num_b = round(num_b)
    return num_a * xa + num_b * xb == xp and num_a * ya + num_b * yb == yp


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
