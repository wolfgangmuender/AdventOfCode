import os
import time

from pulp import LpVariable, LpProblem, LpMinimize, lpSum, PULP_CBC_CMD

TEST_SOLUTION1 = 7
TEST_SOLUTION2 = 33


def solve(puzzle_input):
    machines = []
    for line in puzzle_input:
        machine = {
            "light_diagram": [],
            "buttons": [],
            "joltage": [],
        }
        parts = line.split(" ")
        for part in parts:
            if part.startswith("["):
                machine["light_diagram"] = [True if c == "#" else False for c in part[1:-1]]
            elif part.startswith("("):
                machine["buttons"].append([int(c) for c in part[1:-1].split(",")])
            elif part.startswith("{"):
                machine["joltage"] = [int(c) for c in part[1:-1].split(",")]
            else:
                raise Exception("Whoot?")
        machine["buttons"].sort(key=lambda b: -len(b))
        machines.append(machine)

    total_button_presses1 = 0
    total_button_presses2 = 0
    for machine in machines:
        total_button_presses1 += process_machine_lights(machine)
        total_button_presses2 += process_machine_joltage(machine)

    return total_button_presses1, total_button_presses2


def process_machine_lights(machine):
    end = machine["light_diagram"]

    num_presses = 0
    states = [[False] * len(end)]
    while states:
        num_presses += 1
        new_states = []
        for state in states:
            for button in machine["buttons"]:
                new_state = [not state[i] if i in button else state[i] for i in range(len(state))]
                if new_state == end:
                    return num_presses
                if new_state not in new_states:
                    new_states.append(new_state)
        states = new_states

    raise Exception("Whoot?")


def process_machine_joltage(machine):
    variables = []
    for i in range(len(machine["buttons"])):
        variables.append(LpVariable(f"x{i}", cat="Integer", lowBound=0))

    prob = LpProblem("minimizeJoltage", LpMinimize)
    prob += lpSum(variables)
    for j in range(len(machine["joltage"])):
        prob += lpSum([variables[i] for i in range(len(machine["buttons"])) if j in machine["buttons"][i]]) == machine["joltage"][j]

    prob.solve(PULP_CBC_CMD(msg=False))

    return int(sum([v.varValue for v in variables]))


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
