import os
import time
from collections import defaultdict
from copy import deepcopy


def main(puzzle_input):
    algorithm = None
    input_image = []

    is_first_part = True
    for line in puzzle_input:
        if not line:
            is_first_part = False
        elif is_first_part:
            algorithm = line
        else:
            input_image.append(line)

    curr_default = "."
    initial_image, initial_y_range, initial_x_range = init_image(input_image, curr_default)

    image1 = enhance(initial_image, initial_y_range, initial_x_range, curr_default, algorithm, 2)
    image2 = enhance(initial_image, initial_y_range, initial_x_range, curr_default, algorithm, 50)

    print("Solution 1: {} pixels are lit in the resulting image".format(count_light_pixels(image1)))
    print("Solution 2: {} pixels are lit in the resulting image".format(count_light_pixels(image2)))


def init_image(input_image, curr_default):
    initial_image = defaultdict(lambda: defaultdict(lambda: curr_default))
    initial_x = 0
    initial_y = 0
    for line in input_image:
        initial_x = 0
        for char in line:
            if char == '#':
                initial_image[initial_y][initial_x] = '#'
            initial_x += 1
        initial_y += 1
    return initial_image, list(range(0, initial_y)), list(range(0, initial_x))


def enhance(initial_image, initial_y_range, initial_x_range, curr_default, algorithm, repetitions):
    image = deepcopy(initial_image)
    y_range = initial_y_range
    x_range = initial_x_range
    for i in range(0, repetitions):
        curr_image = image
        image = deepcopy(curr_image)
        y_range = [y_range[0] - 1] + y_range + [y_range[-1] + 1]
        x_range = [x_range[0] - 1] + x_range + [x_range[-1] + 1]
        for y in y_range:
            for x in x_range:
                image[y][x] = determine_output_pixel(curr_image, y, x, algorithm)

        curr_default_pattern = curr_default * 9
        curr_default_index = int(curr_default_pattern.replace(".", "0").replace("#", "1"), 2)
        curr_default = algorithm[curr_default_index]
        image.default_factory = lambda: defaultdict(lambda: curr_default)
        for y in y_range:
            image[y].default_factory = lambda: curr_default

    return image


def determine_output_pixel(curr_image, y, x, algorithm):
    pattern = ""
    for y2 in [y - 1, y, y + 1]:
        for x2 in [x - 1, x, x + 1]:
            pattern += curr_image[y2][x2]
    index = int(pattern.replace(".", "0").replace("#", "1"), 2)
    return algorithm[index]


def count_light_pixels(curr_image):
    count = 0
    for y in curr_image.keys():
        for x in curr_image[y].keys():
            if curr_image[y][x] == "#":
                count += 1
    return count


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
