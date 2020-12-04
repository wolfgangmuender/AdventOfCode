with open("input/input02.txt") as f:
    content = f.read().splitlines()

num_valid1 = 0
num_valid2 = 0
for line in content:
    policy, password = [part.strip() for part in line.split(":")]

    limits = policy[:-2]
    (limit1, limit2) = map(lambda x: int(x), limits.split('-'))
    letter = policy[-1]

    count = password.count(letter)
    if limit1 <= count <= limit2:
        num_valid1 += 1

    match1 = password[limit1 - 1]
    match2 = password[limit2 - 1]
    if (match1 == letter and match2 != letter) or (match1 != letter and match2 == letter):
        num_valid2 += 1

print("Solution 1: {} password are valid!".format(num_valid1))
print("Solution 2: {} password are valid!".format(num_valid2))
