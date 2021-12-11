import itertools
from copy import deepcopy

with open("input/input11.txt") as f:
    content = f.read().splitlines()


def str_to_int_list(the_string):
    return [int(n) for n in list(the_string)]


energy_levels = []
for line in content:
    energy_levels.append(str_to_int_list(line))


def increase_energy_level(the_energy_levels):
    for i in range(0, 10):
        for j in range(0, 10):
            the_energy_levels[i][j] += 1


def flash(the_energy_levels, the_m, the_n):
    the_energy_levels[the_m][the_n] = 0
    for diff in [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]:
        diff_m = the_m + diff[0]
        diff_n = the_n + diff[1]
        if 0 <= diff_m < 10 and 0 <= diff_n < 10 and the_energy_levels[diff_m][diff_n] > 0:
            the_energy_levels[diff_m][diff_n] += 1


energy_levels1 = deepcopy(energy_levels)
num_flashes = 0
for step in range(0, 100):
    increase_energy_level(energy_levels1)

    new_flashes = 'start'
    while new_flashes:
        new_flashes = 0
        for m in range(0, 10):
            for n in range(0, 10):
                if energy_levels1[m][n] > 9:
                    flash(energy_levels1, m, n)
                    num_flashes += 1
                    new_flashes += 1

print("Solution 1: there are {} total flashes after 100 steps".format(num_flashes))

energy_levels2 = deepcopy(energy_levels)
step = 0
while any([el > 0 for el in itertools.chain.from_iterable(energy_levels2)]):
    step += 1
    increase_energy_level(energy_levels2)

    new_flashes = 'start'
    while new_flashes:
        new_flashes = 0
        for m in range(0, 10):
            for n in range(0, 10):
                if energy_levels2[m][n] > 9:
                    flash(energy_levels2, m, n)
                    new_flashes += 1

print("Solution 2: the first step during which all octopuses flash is {}".format(step))
