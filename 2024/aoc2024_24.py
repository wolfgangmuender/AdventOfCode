import os
import time
from copy import deepcopy, copy

TEST_SOLUTION1 = 2024
TEST_SOLUTION2 = ""


def solve(puzzle_input):
    initial_wires = {}
    initial_gates = []
    all_outputs = set()
    for line in puzzle_input:
        if ":" in line:
            wire, value = line.split(": ")
            initial_wires[wire] = bool(int(value))
        elif line:
            gate, output = line.split(" -> ")
            input1, operator, input2 = gate.split(" ")
            input1, input2 = sorted([input1, input2])
            initial_gates.append([operator, input1, input2, output])
            all_outputs.add(output)
    num_bits = int(len(initial_wires) / 2)

    wires = evolve(deepcopy(initial_wires), deepcopy(initial_gates))
    z_wrong = get_number(wires, "z")

    if num_bits > 5:
        mapping = {"fkp": "z06", "z06": "fkp", "ngr": "z11", "z11": "ngr", "mfm": "z31", "z31": "mfm", "krj": "bpt", "bpt": "krj"}
        corrected_gates = map_gates(initial_gates, mapping)
        for i in range(0, num_bits):
            if not check_addition(initial_wires, corrected_gates, num_bits, i):
                print(i)
                break

        relabel(corrected_gates)
    else:
        mapping = {}

    return z_wrong, ",".join(sorted(list(mapping.keys())))


def check_addition(initial_wires, initial_gates, num_bits, i):
    is_correct = True
    for vx, vy, vc in [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]]:
        xx = [0] * num_bits
        xx[i] = vx
        if i > 0:
            xx[i - 1] = vc
        yy = [0] * num_bits
        yy[i] = vy
        if i > 0:
            yy[i - 1] = vc

        x = vx * pow(2, i)
        y = vy * pow(2, i)
        c = 2 * vc * pow(2, i - 1) if i > 0 else 0

        zz = add(initial_wires, initial_gates, xx, yy)
        z = get_number(zz, "z")

        if x + y + c != z:
            is_correct = False

    return is_correct


def add(initial_wires, initial_gates, x, y):
    wires = deepcopy(initial_wires)
    for i in range(0, len(x)):
        wires[f"x{i:02d}"] = x[i]
        wires[f"y{i:02d}"] = y[i]
    gates = deepcopy(initial_gates)
    wires = evolve(wires, gates)
    return wires


def evolve(wires, gates):
    check = 0
    while gates:
        gate = gates.pop(0)
        operator, input1, input2, output = gate
        if input1 in wires and input2 in wires:
            if operator == "AND":
                wires[output] = wires[input1] & wires[input2]
            elif operator == "OR":
                wires[output] = wires[input1] | wires[input2]
            elif operator == "XOR":
                wires[output] = wires[input1] ^ wires[input2]
            check = 0
        else:
            gates.append(gate)
            check += 1

        if check > len(gates):
            break
    return wires


def get_number(wires, prefix):
    the_wires = sorted([wire for wire in wires.keys() if wire.startswith(prefix)])
    output_number = 0
    for i in range(0, len(the_wires)):
        output_number += pow(2, i) if wires[the_wires[i]] else 0

    return output_number


def map_gates(initial_gates, mapping):
    gates_mapped = []
    for gate in initial_gates:
        operator, input1, input2, output = gate
        output = mapping[output] if output in mapping else output
        gates_mapped.append([operator, input1, input2, output])
    return gates_mapped


def relabel(initial_gates):
    mapping = {}
    for gate in initial_gates:
        operator, input1, input2, output = gate
        if input1[1:] == input2[1:]:
            if operator == "AND":
                mapping[output] = f"A{input1[1:]}"
            elif operator == "XOR":
                mapping[output] = f"B{input1[1:]}"
            else:
                raise Exception("Whoot?")

    gates_mapped = []
    for gate in initial_gates:
        operator, input1, input2, output = [mapping[s] if s in mapping else s for s in gate]
        input1, input2 = sorted([input1, input2])
        gates_mapped.append([operator, input1, input2, output])

    for gate in sorted(gates_mapped):
        print(gate)


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
