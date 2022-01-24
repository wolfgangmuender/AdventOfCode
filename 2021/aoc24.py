import os
import time


class Cache:

    def __init__(self):
        self.cache = {}

    def add_to_cache(self, pos, z, res):
        self.cache[Cache.key(pos, z)] = res

    def is_in_cache(self, pos, z):
        return Cache.key(pos, z) in self.cache

    def get_from_cache(self, pos, z):
        return self.cache[Cache.key(pos, z)]

    @staticmethod
    def key(pos, z):
        return "{}_{}".format(pos, z)


def main(puzzle_input):
    instructions = []
    for line in puzzle_input:
        if line.startswith("inp"):
            instructions.append([])
        instructions[-1].append(line.split(" "))

    # checking the instructions it turns out that only z is carried over from pos to pos
    # w is always overridden by input
    # x,y are always multiplied by 0 initially

    model_number = get_largest_model_number(0, instructions, 0, Cache())
    print(model_number)

    print("Solution 1: the largest model number accepted by MONAD is {}".format(model_number))
    print("Solution 2: {}".format(0))


def get_largest_model_number(pos, instructions, z, cache):
    print("{} - {}".format(pos, len(cache.cache.keys())))
    if cache.is_in_cache(pos, z):
        return cache.get_from_cache(pos, z)

    res = None
    for i in reversed(range(1, 10)):
        wxyz = [0, 0, 0, z]
        is_valid = apply_instructions(i, instructions[pos], wxyz)
        if not is_valid:
            continue

        if pos == 13:
            if wxyz[3] == 0:
                res = i
        else:
            sub_res = get_largest_model_number(pos + 1, instructions, wxyz[3], cache)
            if sub_res:
                res = i * 10 ** (13 - pos) + sub_res

    cache.add_to_cache(pos, z, res)
    return res


def apply_instructions(inp, instructions, wxyz):
    for instruction in instructions:
        ind = index(instruction[1])
        if instruction[0] == "inp":
            wxyz[ind] = inp
        elif instruction[0] == "add":
            wxyz[ind] += value(instruction[2], wxyz)
        elif instruction[0] == "mul":
            wxyz[ind] *= value(instruction[2], wxyz)
        elif instruction[0] == "div":
            val = value(instruction[2], wxyz)
            if val == 0:
                return False
            wxyz[ind] = int(wxyz[ind] / val)
        elif instruction[0] == "mod":
            if wxyz[ind] < 0:
                return False
            val = value(instruction[2], wxyz)
            if val <= 0:
                return False
            wxyz[ind] %= val
        elif instruction[0] == "eql":
            val = value(instruction[2], wxyz)
            wxyz[ind] = 1 if wxyz[ind] == val else 0
        else:
            raise Exception("You cannot be serious!")

    return True


def index(var):
    return "wxyz".index(var)


def value(instruction_input, wxyz):
    try:
        return int(instruction_input)
    except ValueError:
        return wxyz[index(instruction_input)]


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
