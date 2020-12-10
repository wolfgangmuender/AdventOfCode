with open("input/input10.txt") as f:
    content = f.read().splitlines()

ratings = []
for line in content:
    ratings.append(int(line))
ratings.sort()

diff1 = 0
diff3 = 0
current_rating = 0
for i in range(0, len(ratings)):
    diff = ratings[i] - current_rating
    if diff == 1:
        diff1 += 1
    elif diff == 3:
        diff3 += 1
    current_rating = ratings[i]
diff3 += 1


def continue_chain(curr):
    if curr in cache:
        return cache[curr]
    elif curr == final_rating:
        return 1
    elif curr not in full_chain:
        return 0
    else:
        num_ways = continue_chain(curr + 1) + continue_chain(curr + 2) + continue_chain(curr + 3)
        cache[curr] = num_ways
        return num_ways


final_rating = ratings[-1] + 3
full_chain = [0] + ratings + [final_rating]
cache = {}
num_chains = continue_chain(0)

print("Solution 1: the number of 1-jolt differences times the number of 3-jolt differences is {}".format(diff1 * diff3))
print("Solution 2: the total number of distinct ways is {}".format(num_chains))
