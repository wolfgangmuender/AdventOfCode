import re

with open("input/input14.txt") as f:
    content = f.read().splitlines()


def string_to_list(the_string):
    the_list = []
    the_list[:0] = the_string
    return the_list


def to_binary_list(int_value, precision):
    return string_to_list(format(int_value, '0' + str(precision) + 'b'))


def to_int(binary_list):
    return int("".join(binary_list), 2)


def apply_bit_mask(the_value, the_mask, ignored_char):
    for i in range(0, len(the_mask)):
        if the_mask[i] != ignored_char:
            the_value[i] = the_mask[i]


mem = {}
mask = None
for line in content:
    command, value = map(lambda x: x.strip(), line.split("="))
    if command == 'mask':
        mask = string_to_list(value)
    elif command.startswith('mem'):
        mem_value = to_binary_list(int(value), 36)
        apply_bit_mask(mem_value, mask, 'X')
        mem_pos = re.compile("^mem\[(\d+)]$").match(command)[1]
        mem[mem_pos] = to_int(mem_value)
    else:
        raise Exception

print("Solution 1: the sum of values in memory is {}".format(sum(mem.values())))

mem = {}
mask = None
for line in content:
    command, value = map(lambda x: x.strip(), line.split("="))
    if command == 'mask':
        mask = string_to_list(value)
    elif command.startswith('mem'):
        mem_value = int(value)
        mem_pos = to_binary_list(int(re.compile("^mem\[(\d+)]$").match(command)[1]), 36)
        apply_bit_mask(mem_pos, mask, '0')
        x_positions = [i for i in range(0, len(mem_pos)) if mem_pos[i] == 'X']
        len_x_positions = len(x_positions)
        for i in range(0, pow(2, len_x_positions)):
            mutators = to_binary_list(i, len_x_positions)
            for (x_position, mutator) in zip(x_positions, mutators):
                mem_pos[x_position] = mutator
            mem[to_int(mem_pos)] = mem_value
    else:
        raise Exception

print("Solution 2: the sum of values in memory is {}".format(sum(mem.values())))
