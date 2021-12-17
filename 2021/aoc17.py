import os
import time


def main(puzzle_input):
    x_string, y_string = puzzle_input[0].replace("target area: ", "").split(", ")
    x_range = [int(x) for x in x_string.replace("x=", "").split("..")]
    y_range = [int(y) for y in y_string.replace("y=", "").split("..")]

    y_max = 0
    velocities = []
    for x_velocity_initial in range(1, x_range[1] + 1):
        for y_velocity_initial in range(-500, 500):
            curr_y_max = 0

            x = 0
            y = 0
            x_velocity = x_velocity_initial
            y_velocity = y_velocity_initial
            while x <= x_range[1] and y >= y_range[0]:
                x += x_velocity
                y += y_velocity
                x_velocity = x_velocity - 1 if x_velocity > 0 else 0
                y_velocity -= 1
                curr_y_max = max(y, curr_y_max)

                if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
                    y_max = max(y_max, curr_y_max)
                    if [x_velocity_initial, y_velocity_initial] not in velocities:
                        velocities.append([x_velocity_initial, y_velocity_initial])

                if x < x_range[0] and x_velocity == 0:
                    break

    print("Solution 1: the highest y position the probe can reach is {}".format(y_max))
    print("Solution 2: there are {} distinct initial velocity values".format(len(velocities)))


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
