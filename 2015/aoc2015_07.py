import os
import time
from copy import deepcopy

TEST_SOLUTION1 = 114
TEST_SOLUTION2 = 114


def solve(puzzle_input):
    instructions = []
    for line in puzzle_input:
        expression, out = line.split(" -> ")
        if "AND" in expression:
            wire1, wire2 = expression.split(" AND ")
            instructions.append({
                "op": "AND",
                "wire1": wire1,
                "wire2": wire2,
                "out": out
            })
        elif "OR" in expression:
            wire1, wire2 = expression.split(" OR ")
            instructions.append({
                "op": "OR",
                "wire1": wire1,
                "wire2": wire2,
                "out": out
            })
        elif "LSHIFT" in expression:
            wire, shift = expression.split(" LSHIFT ")
            instructions.append({
                "op": "LSHIFT",
                "wire": wire,
                "shift": int(shift),
                "out": out
            })
        elif "RSHIFT" in expression:
            wire, shift = expression.split(" RSHIFT ")
            instructions.append({
                "op": "RSHIFT",
                "wire": wire,
                "shift": int(shift),
                "out": out
            })
        elif "NOT" in expression:
            wire = expression[4:]
            instructions.append({
                "op": "NOT",
                "wire": wire,
                "out": out
            })
        else:
            if expression.isnumeric():
                instructions.append({
                    "op": "INPUT",
                    "value": int(expression),
                    "out": out
                })
            else:
                instructions.append({
                    "op": "WIRE",
                    "wire": expression,
                    "out": out
                })

    wires1 = run(list(instructions))
    updated_instructions = deepcopy(instructions)
    for instruction in updated_instructions:
        if instruction["out"] == "b":
            instruction["value"] = wires1["a"]
    wires2 = run(updated_instructions)

    return wires1["a"], wires2["a"]


def run(instructions):
    wires = {}
    while instructions:
        curr = instructions.pop(0)
        if curr["op"] == "INPUT":
            wires[curr["out"]] = curr["value"]
        elif curr["op"] == "WIRE":
            if curr["wire"] in wires:
                wires[curr["out"]] = wires[curr["wire"]]
            else:
                instructions.append(curr)
        elif curr["op"] == "AND":
            if (curr["wire1"] in wires or curr["wire1"] == "1") and curr["wire2"] in wires:
                val = wires[curr["wire1"]] if curr["wire1"] in wires else 1
                wires[curr["out"]] = val & wires[curr["wire2"]]
            else:
                instructions.append(curr)
        elif curr["op"] == "OR":
            if curr["wire1"] in wires and curr["wire2"] in wires:
                wires[curr["out"]] = wires[curr["wire1"]] | wires[curr["wire2"]]
            else:
                instructions.append(curr)
        elif curr["op"] == "LSHIFT":
            if curr["wire"] in wires:
                wires[curr["out"]] = wires[curr["wire"]] << curr["shift"]
            else:
                instructions.append(curr)
        elif curr["op"] == "RSHIFT":
            if curr["wire"] in wires:
                wires[curr["out"]] = wires[curr["wire"]] >> curr["shift"]
            else:
                instructions.append(curr)
        elif curr["op"] == "NOT":
            if curr["wire"] in wires:
                wires[curr["out"]] = ~wires[curr["wire"]]
            else:
                instructions.append(curr)
        else:
            raise Exception("Whoot?")

    return wires


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
