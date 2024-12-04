import os
import time

from pseudo_matrix import PseudoMatrix

TEST_SOLUTION1 = 18
TEST_SOLUTION2 = 9


def solve(puzzle_input):
    word_search = PseudoMatrix(".")
    for line in puzzle_input:
        word_search.append_row(line)

    xmas_count = 0
    for x, y in word_search.iter():
        if word_search[x, y] == "X":
            xmas_count += search_xmas(word_search, x, y)

    x_mas_count = 0
    for x, y in word_search.iter():
        if word_search[x, y] == "A" and search_x_mas(word_search, x, y):
            x_mas_count += 1

    return xmas_count, x_mas_count

def search_xmas(word_search, xs, ys):
    xmas_count = 0

    for xd, yd in [[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]:
        if word_search[xs+xd,ys+yd] == "M" and word_search[xs+2*xd,ys+2*yd] == "A" and word_search[xs+3*xd,ys+3*yd] == "S":
            xmas_count += 1

    return xmas_count

def search_x_mas(word_search, xs, ys):
    x_mas_count = 0

    if (word_search[xs+1,ys+1] == "M" and word_search[xs-1,ys-1] == "S") or (word_search[xs-1,ys-1] == "M" and word_search[xs+1,ys+1] == "S"):
        if (word_search[xs+1,ys-1] == "M" and word_search[xs-1,ys+1] == "S") or (word_search[xs-1,ys+1] == "M" and word_search[xs+1,ys-1] == "S"):
            return True

    return False


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
