import collections

with open("input/input14.txt") as f:
    content = f.read().splitlines()

template = []
rules = {}

template_part = True
for line in content:
    if not line:
        template_part = False
    elif template_part:
        template = list(line)
    else:
        the_pair, the_insertion = line.split(" -> ")
        rules[the_pair] = the_insertion

polymer1 = template
for i in range(0, 10):
    previous_polymer = polymer1
    polymer1 = []

    prev_element = None
    for element in previous_polymer:
        if prev_element:
            polymer1.append(rules["{}{}".format(prev_element, element)])

        polymer1.append(element)
        prev_element = element

counter = collections.Counter(polymer1)
counts = counter.most_common()

print("Solution 1: the quantity of the most common element minus the quantity of the least common element is {}"
      .format(counts[0][1] - counts[-1][1]))

pairs = collections.defaultdict(lambda: 0)
for i in range(len(template) - 1):
    pair = "{}{}".format(template[i], template[i + 1])
    pairs[pair] += 1

for i in range(0, 40):
    curr_pairs = pairs.copy()
    for pair in curr_pairs.keys():
        new = rules[pair]
        pairs[pair] -= curr_pairs[pair]
        pairs["{}{}".format(pair[0], new)] += curr_pairs[pair]
        pairs["{}{}".format(new, pair[1])] += curr_pairs[pair]

counts = collections.defaultdict(lambda: 0)
for pair in pairs:
    counts[pair[0]] += pairs[pair]
counts[template[-1]] += 1
counts = list(counts.values())
counts.sort()

print("Solution 1: the quantity of the most common element minus the quantity of the least common element is {}"
      .format(counts[-1] - counts[0]))
