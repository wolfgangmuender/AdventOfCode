with open("input/input07.txt") as f:
    content = f.read().splitlines()

positions = list(map(lambda x: int(x), content[0].split(",")))

max_pos = max(positions)
min_pos = min(positions)
possible_pos = range(min_pos, max_pos + 1)

fuel_costs1 = []
for align_pos in possible_pos:
    fuel_costs1.append(sum([abs(pos - align_pos) for pos in positions]))

final_fuel_cost1 = min(fuel_costs1)
align_position1 = possible_pos[fuel_costs1.index(final_fuel_cost1)]

print("Solution 1: the crabs need to spend {} fuel to align at position {}".format(final_fuel_cost1, align_position1))

fuel_costs2 = []
for align_pos in possible_pos:
    fuel_costs2.append(sum([int(abs(pos - align_pos) * (abs(pos - align_pos) + 1) / 2) for pos in positions]))

final_fuel_cost2 = min(fuel_costs2)
align_position2 = possible_pos[fuel_costs2.index(final_fuel_cost2)]

print("Solution 2: the crabs need to spend {} fuel to align at position {}".format(final_fuel_cost2, align_position2))
