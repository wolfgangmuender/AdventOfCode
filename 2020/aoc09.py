with open("input/input09.txt") as f:
    content = f.read().splitlines()


def find_summands(number, candidates):
    for can1 in candidates:
        for can2 in candidates:
            if can1 != can2 and can1 + can2 == number:
                return can1, can2

    return None, None


current = None
last_25 = []
numbers = []
for line in content:
    current = int(line)
    if len(last_25) < 25:
        last_25.append(current)
    else:
        num1, num2 = find_summands(current, last_25)
        if not num1 and not num2:
            break
        last_25 = last_25[1:] + [current]
    numbers.append(current)


def check_sum(index):
    candidates = []
    while sum(candidates) < current:
        candidates.append(numbers[index])
        index += 1

    if len(candidates) > 1 and sum(candidates) == current:
        return min(candidates) + max(candidates)

    return None


encryption_weakness = None
start = 0
while encryption_weakness is None:
    encryption_weakness = check_sum(start)
    start += 1

print("Solution 1: the first number that does not sum up is {}".format(current))
print("Solution 2: the encryption weakness is {}".format(encryption_weakness))
