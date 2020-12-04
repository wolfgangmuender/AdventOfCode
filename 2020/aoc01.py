with open("input/input01.txt") as f:
    content = f.read().splitlines()

numbers = [int(line) for line in content]

for n1 in numbers:
    for n2 in numbers:
        if n1 + n2 == 2020:
            print("Solution 1: {} * {} = {}".format(n1, n2, n1 * n2))

for n1 in numbers:
    for n2 in numbers:
        for n3 in numbers:
            if n1 + n2 + n3 == 2020:
                print("Solution 2: {} * {} * {} = {}".format(n1, n2, n3, n1 * n2 * n3))
