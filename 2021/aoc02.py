with open("input/input02.txt") as f:
    content = f.read().splitlines()

commands = []
for line in content:
    command = line.split(' ')
    commands.append({
        'direction': command[0],
        'value': int(command[1]),
    })

pos_h1 = 0
pos_d1 = 0
for command in commands:
    if command['direction'] == 'forward':
        pos_h1 += command['value']
    elif command['direction'] == 'up':
        pos_d1 -= command['value']
    elif command['direction'] == 'down':
        pos_d1 += command['value']
    else:
        raise Exception("Unknown command")

print("Solution 1: the product of the final horizontal position by the final depth is {}".format(pos_h1 * pos_d1))

pos_h2 = 0
pos_d2 = 0
aim = 0
for command in commands:
    if command['direction'] == 'forward':
        pos_h2 += command['value']
        pos_d2 += aim * command['value']
    elif command['direction'] == 'up':
        aim -= command['value']
    elif command['direction'] == 'down':
        aim += command['value']
    else:
        raise Exception("Unknown command")

print("Solution 2: the product of the final horizontal position by the final depth is {}".format(pos_h2 * pos_d2))
