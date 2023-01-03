import os
import time


def solve(puzzle_input):
    print(puzzle_input)
    return 0, 0


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    if os.path.isfile(test_input_file):
        with open(test_input_file) as f:
            content = f.read().splitlines()
        with Timed():
            solution1, solution2 = solve(content)
            if solution1 != 0:
                print("Solution 1 not correct for test input")
                return
            if solution2 != 0:
                print("Solution 2 not correct for test input")
                return
    else:
        open(test_input_file, 'a').close()

    input_file = test_input_file.replace("testinput", "input")
    if os.path.isfile(input_file):
        with open(input_file) as f:
            content = f.read().splitlines()
        with Timed():
            solution1, solution2 = solve(content)
            print("Solution 1: {}".format(solution1))
            print("Solution 2: {}".format(solution2))
    else:
        open(input_file, 'a').close()


class Timed(object):

    def __init__(self):
        self.start = time.time()

    def __enter__(self):
        return self.start

    def __exit__(self, type, value, traceback):
        end = time.time()
        diff = (end - self.start)
        if diff >= 1:
            print("The solutions took {}s".format(round(diff)))
        else:
            print("The solutions took {}ms".format(round(diff * 1000)))
        return True


if __name__ == "__main__":
    main()
