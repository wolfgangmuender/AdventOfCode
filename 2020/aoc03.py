from functools import reduce

with open("input/input03.txt") as f:
    content = f.read().splitlines()

tree_map = content

limit = len(tree_map[0])
diff_x = [1, 3, 5, 7, 1]
diff_y = [1, 1, 1, 1, 2]
num_trees = [0, 0, 0, 0, 0]

for i in range(5):
    x = 0
    y = 0
    while y < len(tree_map) - 1:
        x = (x + diff_x[i]) % limit
        y += diff_y[i]
        if tree_map[y][x] == "#":
            num_trees[i] += 1

print("Solution 1: encountered {} trees".format(num_trees[1]))
print("Solution 2: product of the tree numbers is {}".format(reduce((lambda a, b: a * b), num_trees)))
