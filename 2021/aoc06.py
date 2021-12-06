with open("input/input06.txt") as f:
    content = f.read().splitlines()

initial_reproduction_countdown = list(map(lambda x: int(x), content[0].split(",")))


def reproduce(num_days):
    reproduction_countdown = {}
    for i in range(0, 9):
        reproduction_countdown[i] = sum([1 for rc in initial_reproduction_countdown if rc == i])

    for day in range(0, num_days):
        spawning = reproduction_countdown[0]
        for i in range(1, 9):
            reproduction_countdown[i - 1] = reproduction_countdown[i]
        reproduction_countdown[6] += spawning
        reproduction_countdown[8] = spawning

    return reproduction_countdown


reproduction_countdown1 = reproduce(80)
reproduction_countdown2 = reproduce(256)

print("Solution 1: after 80 days there are {} lanternfish".format(sum(reproduction_countdown1.values())))
print("Solution 2: after 256 days there are {} lanternfish".format(sum(reproduction_countdown2.values())))
