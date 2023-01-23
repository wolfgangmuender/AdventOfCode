import os
import time

TEST_SOLUTION1 = "baedc"


def solve(puzzle_input):
    moves = []
    for move_str in puzzle_input[0].split(","):
        move_id = move_str[0]
        if move_id == "s":
            moves.append({
                "move_id": move_id,
                "diff": int(move_str[1:]),
            })
        elif move_id == "x":
            j1, j2 = [int(i) for i in move_str[1:].split("/")]
            moves.append({
                "move_id": move_id,
                "i1": j1,
                "i2": j2,
            })
        elif move_id == "p":
            name1, name2 = move_str[1:].split("/")
            moves.append({
                "move_id": move_id,
                "name1": name1,
                "name2": name2,
            })
        else:
            raise Exception("Whoot?")

    if len(moves) == 3:
        # test special handling
        programs = list("abcde")
    else:
        programs = list("abcdefghijklmnop")

    all_programs = [programs]

    programs, next_programs = dance(moves, programs)
    all_programs.extend(next_programs)
    solution1 = "".join(programs)

    for i in range(1, 100):
        programs, next_programs = dance(moves, programs)
        all_programs.extend(next_programs)

    cycle_length = None
    for i in range(1, 99):
        if all_programs[0] == all_programs[i * len(moves)]:
            cycle_length = i
            break

    total_dances = 1000000000
    remaining_dances = total_dances % cycle_length

    solution2 = "".join(all_programs[remaining_dances * len(moves)])

    return solution1, solution2


def dance(moves, programs):
    all_programs = []
    for move in moves:
        if move["move_id"] == "s":
            s = move["diff"]
            programs = programs[-s:] + programs[:-s]
        elif move["move_id"] == "x":
            i1 = move["i1"]
            i2 = move["i2"]
            j1 = i1 if i1 < i2 else i2
            j2 = i2 if i1 < i2 else i1
            programs = programs[:j1] + [programs[j2]] + programs[j1 + 1:j2] + [programs[j1]] + programs[j2 + 1:]
        elif move["move_id"] == "p":
            i1 = programs.index(move["name1"])
            i2 = programs.index(move["name2"])
            j1 = i1 if i1 < i2 else i2
            j2 = i2 if i1 < i2 else i1
            programs = programs[:j1] + [programs[j2]] + programs[j1 + 1:j2] + [programs[j1]] + programs[j2 + 1:]
        else:
            raise Exception("Whoot?")

        all_programs.append(programs)

    return programs, all_programs


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
