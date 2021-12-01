with open("input/input01.txt") as f:
    content = f.read().splitlines()

depth_measurements = [int(line) for line in content]


def sum3(the_list, the_index):
    return the_list[the_index] + the_list[the_index + 1] + the_list[the_index + 2]


slopes = [depth_measurements[n] - depth_measurements[n - 1] for n in range(1, len(depth_measurements))]
slopes3 = [sum3(depth_measurements, n) - sum3(depth_measurements, n-1) for n in range(1, len(depth_measurements) - 2)]

print("Solution 1: it goes down {} times".format(sum(n > 0 for n in slopes)))
print("Solution 2: it goes down {} times".format(sum(n > 0 for n in slopes3)))
