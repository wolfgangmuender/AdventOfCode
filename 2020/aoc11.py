from collections import defaultdict

from copy import deepcopy

with open("input/input11.txt") as f:
    content = f.read().splitlines()

seat_layout = defaultdict(lambda: defaultdict(lambda: '.'))
curr_line = 0
curr_pos = 0
for line in content:
    curr_pos = 0
    for char in line:
        seat_layout[curr_line][curr_pos] = char
        curr_pos += 1
    curr_line += 1
num_rows = curr_line
row_len = curr_pos


def count_adjacent_seats(seat_layout_to_test, y, x, char):
    return (
            seat_layout_to_test[y - 1][x - 1] + seat_layout_to_test[y - 1][x] + seat_layout_to_test[y - 1][x + 1]
            + seat_layout_to_test[y][x - 1] + seat_layout_to_test[y][x + 1]
            + seat_layout_to_test[y + 1][x - 1] + seat_layout_to_test[y + 1][x] + seat_layout_to_test[y + 1][x + 1]
    ).count(char)


num_seats = 0
seat_layout_next = deepcopy(seat_layout)
while True:
    seat_layout_curr = seat_layout_next
    seat_layout_next = deepcopy(seat_layout_curr)
    num_seats_next = 0
    for i in range(0, num_rows):
        for j in range(0, row_len):
            if seat_layout_curr[i][j] == 'L' and count_adjacent_seats(seat_layout_curr, i, j, '#') == 0:
                seat_layout_next[i][j] = '#'
            if seat_layout_curr[i][j] == '#' and count_adjacent_seats(seat_layout_curr, i, j, '#') >= 4:
                seat_layout_next[i][j] = 'L'
            num_seats_next += 1 if seat_layout_next[i][j] == '#' else 0
    if num_seats == num_seats_next:
        break
    num_seats = num_seats_next

print("Solution 1: {} seats end up occupied".format(num_seats))


def find_visible_seat(seat_layout_to_test, y, x, diff_y, diff_x):
    curr_y = y + diff_y
    curr_x = x + diff_x
    while (0 <= curr_y < num_rows) and (0 <= curr_x < row_len):
        curr = seat_layout_to_test[curr_y][curr_x]
        if curr != '.':
            return curr
        curr_y = curr_y + diff_y
        curr_x = curr_x + diff_x
    return '.'


def count_visible_seats(seat_layout_to_test, y, x, char):
    return (
            find_visible_seat(seat_layout_to_test, y, x, -1, -1)
            + find_visible_seat(seat_layout_to_test, y, x, -1, 0)
            + find_visible_seat(seat_layout_to_test, y, x, -1, 1)
            + find_visible_seat(seat_layout_to_test, y, x, 0, -1)
            + find_visible_seat(seat_layout_to_test, y, x, 0, 1)
            + find_visible_seat(seat_layout_to_test, y, x, 1, -1)
            + find_visible_seat(seat_layout_to_test, y, x, 1, 0)
            + find_visible_seat(seat_layout_to_test, y, x, 1, 1)
    ).count(char)


num_seats = 0
seat_layout_next = seat_layout
while True:
    seat_layout_curr = seat_layout_next
    seat_layout_next = deepcopy(seat_layout_curr)
    num_seats_next = 0
    for i in range(0, num_rows):
        for j in range(0, row_len):
            if seat_layout_curr[i][j] == 'L' and count_visible_seats(seat_layout_curr, i, j, '#') == 0:
                seat_layout_next[i][j] = '#'
            if seat_layout_curr[i][j] == '#' and count_visible_seats(seat_layout_curr, i, j, '#') >= 5:
                seat_layout_next[i][j] = 'L'
            num_seats_next += 1 if seat_layout_next[i][j] == '#' else 0
    if num_seats == num_seats_next:
        break
    num_seats = num_seats_next

print("Solution 2: {} seats end up occupied".format(num_seats))
