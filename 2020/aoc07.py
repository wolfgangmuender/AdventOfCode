from collections import defaultdict

with open("input/input07.txt") as f:
    content = f.read().splitlines()

rules = {}
reversed_rules = defaultdict(list)
for line in content:
    color, bags = map(lambda x: x.strip(), line[:-1].split("bags contain"))
    rules[color] = {}
    if "no other" in bags:
        continue
    for bag in map(lambda x: x.strip(), bags.split(", ")):
        bag_info = bag.split(' ')
        bag_color = ' '.join(bag_info[1:-1])
        rules[color][bag_color] = int(bag_info[0])
        reversed_rules[bag_color].append(color)


def add_bags_recursively(bags_to_add):
    for bag in bags_to_add:
        if bag in encasing_bags:
            continue
        else:
            encasing_bags.add(bag)
            add_bags_recursively(reversed_rules[bag])


def sum_bags_recursively(bags):
    return sum(map(lambda bag: bags[bag] * (1 + sum_bags_recursively(rules[bag])), bags.keys()))


color_to_find = "shiny gold"
encasing_bags = set()
add_bags_recursively(reversed_rules[color_to_find])
num_bags = sum_bags_recursively(rules[color_to_find])

print("Solution 1: {} bag colors can eventually contain one {} bag".format(len(encasing_bags), color_to_find))
print("Solution 2: {} bags are required inside one {} bag".format(num_bags, color_to_find))
