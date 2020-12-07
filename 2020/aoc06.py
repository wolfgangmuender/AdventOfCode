from functools import reduce

with open("input/input06.txt") as f:
    content = f.read().splitlines()

anyone_yes_answers = [set()]
everyone_yes_answers = [set()]
is_new = True
for line in content:
    if line:
        for char in line:
            anyone_yes_answers[-1].add(char)
        if is_new:
            for char in line:
                everyone_yes_answers[-1].add(char)
            is_new = False
        else:
            for char in list(everyone_yes_answers[-1]):
                if char not in line:
                    everyone_yes_answers[-1].remove(char)
    else:
        anyone_yes_answers.append(set())
        everyone_yes_answers.append(set())
        is_new = True

print("Solution 1: the sum of anyone yes answers is {}".format(
    reduce(lambda x, y: x + y, map(lambda x: len(x), anyone_yes_answers))))
print("Solution 2: the sum of everyone yes answers is {}".format(
    reduce(lambda x, y: x + y, map(lambda x: len(x), everyone_yes_answers))))
