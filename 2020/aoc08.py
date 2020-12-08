with open("input/input08.txt") as f:
    content = f.read().splitlines()

pos = 0
commands = {}
for line in content:
    command, value = line.split(" ")
    commands[pos] = {
        "command": command,
        "value": int(value)
    }
    pos += 1
num_commands = pos


def run(commands_copy):
    accumulator = 0

    current = None
    visited = []
    while current not in visited:
        if current is None:
            current = 0
            continue
        if current >= num_commands:
            break

        visited.append(current)
        if commands_copy[current]["command"] == "acc":
            accumulator += commands_copy[current]["value"]
            current += 1
        elif commands_copy[current]["command"] == "jmp":
            current += commands_copy[current]["value"]
        elif commands_copy[current]["command"] == "nop":
            current += 1
        else:
            raise Exception

    return accumulator, current


def mutate():
    for mutation_index in range(0, num_commands):
        original_command = commands[mutation_index]["command"]
        if original_command == "acc":
            continue

        commands_copy = dict(commands)
        commands_copy[mutation_index] = {
            "command": "nop" if original_command == "jmp" else "jmp",
            "value": commands[mutation_index]["value"]
        }
        accumulator, current = run(commands_copy)
        if current >= num_commands:
            return accumulator

    raise Exception


print("Solution 1: the value of the accumulator is {}".format(run(commands)[0]))
print("Solution 2: the value of the accumulator is {}".format(mutate()))
