import os
import time
from math import floor


def main(puzzle_input):
    from input.input11 import monkeys

    for monkey in monkeys:
        monkey.init()

    curr_round = 0
    while curr_round < 20:
        for monkey in monkeys:
            while monkey.items:
                monkey.inspections += 1
                old = monkey.items.pop(0)
                new = _manage_worry(monkey.compute(old), None)
                next_monkey = monkey.next_monkey(new)
                monkeys[next_monkey].items.append(new)

        curr_round += 1

    print("Solution 1: {}".format(_get_monkey_business(monkeys)))

    total_mod = 1
    for monkey in monkeys:
        monkey.init()
        total_mod *= monkey.mod

    curr_round = 0
    while curr_round < 10000:
        for monkey in monkeys:
            while monkey.items:
                monkey.inspections += 1
                old = monkey.items.pop(0)
                new = _manage_worry(monkey.compute(old), total_mod)
                next_monkey = monkey.next_monkey(new)
                monkeys[next_monkey].items.append(new)

        curr_round += 1

    print("Solution 2: {}".format(_get_monkey_business(monkeys)))


def _manage_worry(worry_level, total_mod):
    if total_mod:
        return worry_level % total_mod
    else:
        return floor(worry_level / 3)


def _get_monkey_business(monkeys):
    inspections = [monkey.inspections for monkey in monkeys]
    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


if __name__ == "__main__":
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    main(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))
