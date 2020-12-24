import time
from copy import copy

with open("input/input23.txt") as f:
    content = f.read().splitlines()


def string_to_list(the_string):
    the_list = []
    the_list[:0] = the_string
    return the_list


initial_cups = list(map(lambda x: int(x), string_to_list(content[0])))


def play(cups, rounds):
    start = time.time()
    current_cup = cups[0]
    for i in range(0, rounds):
        if i > 0 and i % 1000 == 0:
            print(i)
            print(time.time() - start)
        current_index = cups.index(current_cup)
        cups = cups[current_index:] + cups[0:current_index]

        stash = [cups.pop(1) for j in range(0, 3)]

        destination_cup = current_cup - 1
        while destination_cup not in cups:
            destination_cup -= 1
            if destination_cup <= 0:
                destination_cup = 9

        current_index = cups.index(destination_cup)
        for j in range(0, 3):
            cups.insert(current_index + 1 + j, stash[j])

        current_cup = cups[1]

    return cups


final_cups = play(copy(initial_cups), 100)
labels = final_cups[final_cups.index(1) + 1:] + final_cups[0:final_cups.index(1)]

print("Solution 1: the labels on the cups after cup 1 are {}".format("".join([str(label) for label in labels])))

initial_cups_large = initial_cups + list(range(len(initial_cups) + 1, 1000001))
final_cups_large = play(copy(initial_cups_large), 10000000)
index_1 = final_cups.index(1)

# no result, takes way too long :/
print("Solution 2: the product of the star cups labels is {}".format(
    final_cups_large[index_1 + 1] * final_cups_large[index_1 + 2]))
