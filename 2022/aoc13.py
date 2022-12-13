import json
import os
import time
from functools import cmp_to_key


def main(puzzle_input):
    packets = []
    for line in puzzle_input:
        if line:
            packets.append(json.loads(line))

    right_order_pairs = []
    for i in range(0, len(packets), 2):
        if _compare(packets[i], packets[i + 1]) == 1:
            right_order_pairs.append(int(i/2+1))

    print("Solution 1: {}".format(sum(right_order_pairs)))

    divider1 = [[2]]
    divider2 = [[6]]
    all_packets = packets + [divider1, divider2]
    all_packets.sort(key=cmp_to_key(_compare), reverse=True)

    print("Solution 2: {}".format((all_packets.index(divider1)+1)*(all_packets.index(divider2)+1)))


def _compare(left, right):
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return 1
            elif left > right:
                return -1
            else:
                return 0
        else:
            return _compare([left], right)
    else:
        if isinstance(right, int):
            return _compare(left, [right])
        else:
            max_len = min(len(left), len(right))
            for i in range(0, max_len):
                compare = _compare(left[i], right[i])
                if compare != 0:
                    return compare
            if len(left) < len(right):
                return 1
            elif len(right) < len(left):
                return -1
            else:
                return 0




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
