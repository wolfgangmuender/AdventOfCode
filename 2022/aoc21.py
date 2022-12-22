import os
import time


def solve(puzzle_input):
    monkeys = {}
    for line in puzzle_input:
        monkey_name, job = line.split(": ")
        if "+" in job:
            monkeys[monkey_name] = _parse_job(job, "+")
        elif "-" in job:
            monkeys[monkey_name] = _parse_job(job, "-")
        elif "*" in job:
            monkeys[monkey_name] = _parse_job(job, "*")
        elif "/" in job:
            monkeys[monkey_name] = _parse_job(job, "/")
        else:
            monkeys[monkey_name] = {"number": int(job)}

    print("Solution 1: {}".format(_yell(monkeys, "root")))

    print("Solution 2: {}".format(_determine_human_yell(monkeys)))


def _yell(monkeys, monkey_name):
    if "number" in monkeys[monkey_name]:
        return monkeys[monkey_name]["number"]
    else:
        monkeys[monkeys[monkey_name]["monkey1"]]["caller"] = monkey_name
        monkeys[monkeys[monkey_name]["monkey2"]]["caller"] = monkey_name
        if monkeys[monkey_name]["operator"] == "+":
            return _yell(monkeys, monkeys[monkey_name]["monkey1"]) + _yell(monkeys, monkeys[monkey_name]["monkey2"])
        elif monkeys[monkey_name]["operator"] == "-":
            return _yell(monkeys, monkeys[monkey_name]["monkey1"]) - _yell(monkeys, monkeys[monkey_name]["monkey2"])
        elif monkeys[monkey_name]["operator"] == "*":
            return _yell(monkeys, monkeys[monkey_name]["monkey1"]) * _yell(monkeys, monkeys[monkey_name]["monkey2"])
        elif monkeys[monkey_name]["operator"] == "/":
            return int(_yell(monkeys, monkeys[monkey_name]["monkey1"]) / _yell(monkeys, monkeys[monkey_name]["monkey2"]))
        else:
            raise Exception("Whoot?")


def _determine_human_yell(monkeys):
    hierarchy = ["humn"]
    curr_name = monkeys["humn"]
    while "caller" in curr_name:
        caller_name = curr_name["caller"]
        hierarchy.append(caller_name)
        curr_name = monkeys[caller_name]

    expected_result = None
    while hierarchy:
        curr_name = hierarchy.pop()
        target_name = hierarchy[-1]
        expected_result = _invert(monkeys, curr_name, target_name, expected_result)

        if target_name == "humn":
            return expected_result

    raise Exception("Whoot?")


def _invert(monkeys, curr_name, target_name, expected_result):
    curr = monkeys[curr_name]
    target_key, other_key = ("monkey1", "monkey2") if curr["monkey1"] == target_name else ("monkey2", "monkey1")

    if curr_name == "root":
        return _yell(monkeys, curr[other_key])

    if curr["operator"] == "+":
        return expected_result - _yell(monkeys, curr[other_key])
    elif curr["operator"] == "-":
        if target_key == "monkey1":
            return expected_result + _yell(monkeys, curr[other_key])
        else:
            return _yell(monkeys, curr[other_key]) - expected_result
    elif curr["operator"] == "*":
        return int(expected_result / _yell(monkeys, curr[other_key]))
    elif curr["operator"] == "/":
        if target_key == "monkey1":
            return expected_result * _yell(monkeys, curr[other_key])
        else:
            return int(_yell(monkeys, curr[other_key]) / expected_result)

    raise Exception("Whoot?")


def _parse_job(job, operator):
    monkey1, monkey2 = job.split(" " + operator + " ")
    return {
        "monkey1": monkey1,
        "monkey2": monkey2,
        "operator": operator
    }


def main():
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    solve(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))


if __name__ == "__main__":
    main()
