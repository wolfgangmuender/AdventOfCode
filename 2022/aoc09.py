import os
import time


def main(puzzle_input):
    motions = []
    for line in puzzle_input:
        direction, steps = line.split(" ")
        motions.append([direction, int(steps)])

    head = [0, 0]
    tail = [0, 0]
    visited = [[0, 0]]
    for motion in motions:
        direction, steps = motion
        for i in range(0, steps):
            head = _move_head(head, direction)
            tail = _follow(head, tail)
            if tail not in visited:
                visited.append(tail)

    print("Solution 1: {}".format(len(visited)))

    rope = [[0, 0] for _ in range(0, 10)]
    visited = [[0, 0]]
    for motion in motions:
        direction, steps = motion
        for i in range(0, steps):
            rope[0] = _move_head(rope[0], direction)
            for j in range(1,10):
                rope[j] = _follow(rope[j-1], rope[j])
            if rope[-1] not in visited:
                visited.append(rope[-1])

    print("Solution 2: {}".format(len(visited)))


def _move_head(head, direction):
    if direction == "R":
        return [head[0]+1, head[1]]
    elif direction == "L":
        return [head[0]-1, head[1]]
    elif direction == "U":
        return [head[0], head[1]+1]
    elif direction == "D":
        return [head[0], head[1]-1]
    else:
        raise Exception("Whoot!")


def _follow(header, follower):
    diff_x = header[0] - follower[0]
    diff_y = header[1] - follower[1]

    if abs(diff_x) <= 1 and abs(diff_y) <= 1:
        return follower

    if diff_x == 0:
        y = header[1] - 1 if header[1] > follower[1] else header[1] + 1
        return [header[0], y]

    if diff_y == 0:
        x = header[0] - 1 if header[0] > follower[0] else header[0] + 1
        return [x, header[1]]

    x = follower[0] + 1 if header[0] > follower[0] else follower[0] - 1
    y = follower[1] + 1 if header[1] > follower[1] else follower[1] - 1

    return [x,y]


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
