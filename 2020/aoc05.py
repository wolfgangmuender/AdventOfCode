from math import floor, ceil

with open("input/input05.txt") as f:
    content = f.read().splitlines()

seat_ids = []
for line in content:
    row_min = 0
    row_max = 127
    seat_min = 0
    seat_max = 7
    for c in line:
        if c == "F":
            row_max = floor((row_min + row_max) / 2)
        elif c == "B":
            row_min = ceil((row_min + row_max) / 2)
        elif c == "L":
            seat_max = floor((seat_min + seat_max) / 2)
        elif c == "R":
            seat_min = ceil((seat_min + seat_max) / 2)
    seat_ids.append(row_min * 8 + seat_min)

print("Solution 1: the highest seat ID is {}".format(max(seat_ids)))

for i in range(min(seat_ids), max(seat_ids)):
    if i not in seat_ids:
        print("Solution 2: your seat ID is {}".format(i))
        break
