import time
from copy import copy

with open("input/input13.txt") as f:
    content = f.read().splitlines()

earliest_departure = int(content[0])
bus_ids = [int(val) for val in content[1].split(',') if val != 'x']

earliest_bus_id = None
minutes_to_wait = None
for bus_id in bus_ids:
    minutes_late = earliest_departure % bus_id
    curr_minutes_to_wait = minutes_late if minutes_late == 0 else bus_id - minutes_late
    if not minutes_to_wait or curr_minutes_to_wait < minutes_to_wait:
        earliest_bus_id = bus_id
        minutes_to_wait = curr_minutes_to_wait

print("Solution 1: the earliest buses id {} times minutes to wait {} is {}"
      .format(earliest_bus_id, minutes_to_wait, earliest_bus_id * minutes_to_wait))



bus_ids = {}
count = 0
for val in content[1].split(','):
    if val != 'x':
        bus_ids[int(val)] = count
    count += 1
inverted = {v: k for k, v in bus_ids.items()}
max_delay = max(inverted.keys())

print(bus_ids)
print(max_delay)

relevant_schedule = copy(inverted)
for bus_id in bus_ids.keys():
    print(bus_id)
    delay = bus_ids[bus_id]
    while delay < max_delay:
        delay += bus_id
        if delay in inverted:
            relevant_schedule[delay] = relevant_schedule[delay] * bus_id

relevant_check = {v: k for k, v in relevant_schedule.items()}
max_cycle = max(relevant_check)

earliest_timestamp = None
count = 1
while True:
    earliest_timestamp = count*max_cycle-relevant_check[max_cycle]
    check = [(earliest_timestamp + bus_ids[bus_id]) % bus_id for bus_id in bus_ids.keys()]
    if sum(check) == 0:
        break
    count += 1
end = time.time()

print("Solution 2: {}".format(earliest_timestamp))
