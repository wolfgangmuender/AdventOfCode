import os
import time

TEST_SOLUTION1 = "5,7,3,0"
TEST_SOLUTION2 = 117440


def solve(puzzle_input):
    initial_registers = []
    program = []
    for line in puzzle_input:
        if line.startswith("Register A: "):
            initial_registers.append(int(line.replace("Register A: ", "")))
        elif line.startswith("Register B: "):
            initial_registers.append(int(line.replace("Register B: ", "")))
        elif line.startswith("Register C: "):
            initial_registers.append(int(line.replace("Register C: ", "")))
        elif line.startswith("Program: "):
            program = [int(n) for n in line.replace("Program: ", "").split(",")]

    output = run_program([n for n in initial_registers], program)

    a = 0
    curr = None
    while curr != program:
        registers = [a, initial_registers[1], initial_registers[2]]
        curr = run_program(registers, program)
        if curr == program:
            break

        for i in reversed(range(0, len(program))):
            if i >= len(curr) or curr[i] != program[i]:
                a += pow(8, i)
                break

    return ",".join([str(o) for o in output]), a


def run_program(registers, program):
    output = []
    i = 0
    while i < len(program):
        opcode = program[i]
        operand = program[i + 1]
        combo_operand = get_combo_operand(operand, registers)
        if opcode == 0:
            registers[0] = int(registers[0] / pow(2, combo_operand))
        elif opcode == 1:
            registers[1] = registers[1] ^ operand
        elif opcode == 2:
            registers[1] = combo_operand % 8
        elif opcode == 3:
            if registers[0] != 0:
                i = operand
                continue
        elif opcode == 4:
            registers[1] = registers[1] ^ registers[2]
        elif opcode == 5:
            output.append(combo_operand % 8)
        elif opcode == 6:
            registers[1] = int(registers[0] / pow(2, combo_operand))
        elif opcode == 7:
            registers[2] = int(registers[0] / pow(2, combo_operand))

        i += 2

    return output


def get_combo_operand(combo, registers):
    if 0 <= combo <= 3:
        return combo
    elif combo == 4:
        return registers[0]
    elif combo == 5:
        return registers[1]
    elif combo == 6:
        return registers[2]
    else:
        return None


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
