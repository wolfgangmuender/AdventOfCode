import os
import time
from collections import defaultdict

TEST_SOLUTION1 = 4


def solve(puzzle_input):
    instructions = []
    for line in puzzle_input:
        instructions.append(line.split(" "))

    outbox = []
    apply_instructions(instructions, defaultdict(lambda: 0), 0, [], outbox, False)
    solution1 = outbox[-1]

    registers0 = defaultdict(lambda: 0)
    registers0["p"] = 0
    registers1 = defaultdict(lambda: 0)
    registers1["p"] = 1
    outbox0 = []
    outbox1 = []
    curr0 = 0
    curr1 = 0

    total_sent = 0

    while 0 <= curr0 < len(instructions) or 0 <= curr1 < len(instructions):
        curr0 = apply_instructions(instructions, registers0, curr0, outbox1, outbox0, True)

        len_before = len(outbox1)
        curr1 = apply_instructions(instructions, registers1, curr1, outbox0, outbox1, True)
        total_sent += len(outbox1) - len_before

        if not outbox0 and not outbox1:
            break

    return solution1, total_sent


def apply_instructions(instructions, registers, curr, inbox, outbox, correct_instructions):
    while 0 <= curr < len(instructions):
        instruction = instructions[curr]
        cmd = instruction[0]
        if cmd == "snd":
            outbox.append(get_value(instruction[1], registers))
            curr += 1
        elif cmd == "set":
            registers[instruction[1]] = get_value(instruction[2], registers)
            curr += 1
        elif cmd == "add":
            registers[instruction[1]] += get_value(instruction[2], registers)
            curr += 1
        elif cmd == "mul":
            registers[instruction[1]] *= get_value(instruction[2], registers)
            curr += 1
        elif cmd == "mod":
            registers[instruction[1]] %= get_value(instruction[2], registers)
            curr += 1
        elif cmd == "rcv":
            if correct_instructions:
                if inbox:
                    registers[instruction[1]] = inbox.pop(0)
                else:
                    break
            else:
                if get_value(instruction[1], registers) != 0:
                    break
            curr += 1
        elif cmd == "jgz":
            if get_value(instruction[1], registers) > 0:
                curr += get_value(instruction[2], registers)
            else:
                curr += 1
        else:
            raise Exception("Whoot?")

    return curr


def get_value(value, registers):
    try:
        return int(value)
    except ValueError:
        return registers[value]


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
