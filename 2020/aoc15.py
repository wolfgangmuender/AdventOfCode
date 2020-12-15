with open("input/input15.txt") as f:
    content = f.read().splitlines()


def get_last_number_spoken(length):
    numbers = list(map(lambda x: int(x), content[0].split(",")))
    last_spoken_indexes = {k: [v] for v, k in enumerate(numbers)}
    while len(numbers) < length:
        last_spoken_number = numbers[-1]
        last_spoken_index = last_spoken_indexes[last_spoken_number]
        if len(last_spoken_index) == 1:
            next_number = 0
        else:
            next_number = last_spoken_index[1] - last_spoken_index[0]
        numbers.append(next_number)
        if next_number not in last_spoken_indexes:
            last_spoken_indexes[next_number] = [len(numbers) - 1]
        elif len(last_spoken_indexes[next_number]) == 1:
            last_spoken_indexes[next_number] = [last_spoken_indexes[next_number][0], len(numbers) - 1]
        else:
            last_spoken_indexes[next_number] = [last_spoken_indexes[next_number][1], len(numbers) - 1]

    return numbers[-1]


print("Solution 1: the 2020th number spoken is {}".format(get_last_number_spoken(2020)))
print("Solution 2: the 2020th number spoken is {}".format(get_last_number_spoken(30000000)))
