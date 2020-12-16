from copy import copy
from functools import reduce

with open("input/input16.txt") as f:
    content = f.read().splitlines()


def separated_string_to_list_of_int(the_string, separator):
    return list(map(lambda x: int(x), the_string.split(separator)))


def split_and_strip(the_string, separator):
    return [part.strip() for part in the_string.split(separator)]


field_rules = {}
your_ticket = None
nearby_tickets = []
phase = 0
for line in content:
    if not line:
        continue
    elif line in ["your ticket:", "nearby tickets:"]:
        phase += 1
        continue

    if phase == 0:
        field, ranges_string = split_and_strip(line, ":")
        ranges_list = split_and_strip(ranges_string, "or")
        field_rules[field] = list(
            map(lambda range_string: separated_string_to_list_of_int(range_string, "-"), ranges_list))
    elif phase == 1:
        your_ticket = separated_string_to_list_of_int(line, ",")
    elif phase == 2:
        nearby_tickets.append(separated_string_to_list_of_int(line, ","))
    else:
        raise Exception


def contained_in_limits(rule_to_check, value):
    for limits in rule_to_check:
        if value in range(limits[0], limits[1] + 1):
            return True
    return False


invalid_values = []
valid_tickets = []
for nearby_ticket in nearby_tickets:
    values_to_check = copy(nearby_ticket)
    for field, rule in field_rules.items():
        for value_to_check in values_to_check:
            if contained_in_limits(rule, value_to_check):
                values_to_check.remove(value_to_check)
    if values_to_check:
        invalid_values.extend(values_to_check)
    else:
        valid_tickets.append(nearby_ticket)

num_fields = len(field_rules.keys())

field_matches = {}
for field, rule in field_rules.items():
    all_matching = list(range(0, num_fields))
    for valid_ticket in valid_tickets:
        for i in range(0, num_fields):
            if not contained_in_limits(rule, valid_ticket[i]):
                all_matching.remove(i)
    field_matches[field] = all_matching

field_map = {}
departure_indexes = []
while len(field_matches):
    current_index = None
    for field, field_match in field_matches.items():
        if len(field_match) == 1:
            current_index = field_match[0]
            field_map[field] = current_index
            if "departure" in field:
                departure_indexes.append(current_index)
            del field_matches[field]
            break
    for field, field_match in field_matches.items():
        field_match.remove(current_index)

print(field_map)
print(departure_indexes)
print(your_ticket)

print("Solution 1: the ticket scanning error rate is {}".format(sum(invalid_values)))
print("Solution 2: the product of the departure-related field values is {}"
      .format(reduce(lambda x, y: x * y, [your_ticket[i] for i in departure_indexes])))
