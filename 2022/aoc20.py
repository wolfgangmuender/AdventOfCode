import os
import time


def solve(puzzle_input):
    numbers = [int(line) for line in puzzle_input]

    print("Solution 1: {}".format(_mix(numbers, 1)))

    decryption_key = 811589153
    new_numbers = [num*decryption_key for num in numbers]

    print("Solution 2: {}".format(_mix(new_numbers, 10)))


def _mix(numbers, rounds):
    nlen = len(numbers)
    indexes = list(range(0, nlen))
    for _ in range(0, rounds):
        for i in range(0, nlen):
            num = numbers[i]
            if abs(num) % (nlen-1) == 0:
                continue

            old = indexes[i]
            shift = num % (nlen-1) if num >= 0 else - (-num % (nlen-1))
            if shift > 0:
                if old + shift >= len(numbers) - 1:
                    new = (old + shift + 1) % len(numbers)
                else:
                    new = old + shift
            else:
                if old + shift > 0:
                    new = old + shift
                else:
                    new = (old + shift - 1) % len(numbers)
            if new > old:
                indexes[i] = new
                for j in range(0, len(indexes)):
                    if i != j and old < indexes[j] <= new:
                        indexes[j] -= 1
            else:
                indexes[i] = new
                for j in range(0, len(indexes)):
                    if i != j and new <= indexes[j] < old:
                        indexes[j] += 1

    null_index = numbers.index(0)
    index1 = indexes.index((indexes[null_index] + 1000) % len(numbers))
    index2 = indexes.index((indexes[null_index] + 2000) % len(numbers))
    index3 = indexes.index((indexes[null_index] + 3000) % len(numbers))

    return numbers[index1] + numbers[index2] + numbers[index3]


def _print(numbers, indexes):
    print([num for _, num in sorted(zip(indexes, numbers))])


def main():
    input_filename = os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    with open("input/{}".format(input_filename)) as f:
        content = f.read().splitlines()

    start = time.time()
    solve(content)
    end = time.time()
    diff = (end - start)
    if diff >= 1:
        print("The solutions took {}s".format(round(diff)))
    else:
        print("The solutions took {}ms".format(round(diff * 1000)))


if __name__ == "__main__":
    main()
