import os
import time

TEST_SOLUTION1 = 2
TEST_SOLUTION2 = 1

INFO = {"children": 3, "cats": 7, "samoyeds": 2, "pomeranians": 3, "akitas": 0, "vizslas": 0, "goldfish": 5, "trees": 3, "cars": 2, "perfumes": 1}


def solve(puzzle_input):
    aunts = []
    for line in puzzle_input:
        aunt = {}
        for info in line[line.index(" ", 5) + 1:].split(", "):
            prop, num = info.split(": ")
            aunt[prop] = int(num)
        aunts.append(aunt)

    the_aunt = None
    the_real_aunt = None
    for i in range(0, len(aunts)):
        if check(aunts[i], False):
            the_aunt = i
        if check(aunts[i], True):
            the_real_aunt = i
        if the_aunt and the_real_aunt:
            break

    return the_aunt + 1, the_real_aunt + 1


def check(aunt, is_real):
    for prop, value in aunt.items():
        if is_real:
            if prop in ["cats", "trees"]:
                if value <= INFO[prop]:
                    return False
            elif prop in ["pomeranians", "goldfish"]:
                if value >= INFO[prop]:
                    return False
            else:
                if value != INFO[prop]:
                    return False
        else:
            if value != INFO[prop]:
                return False
    return True


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
