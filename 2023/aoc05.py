import os
import time

TEST_SOLUTION1 = 35
TEST_SOLUTION2 = 46


class KeyDefaultDict:

    def __init__(self):
        self.mappings = []

    def add_mapping(self, drs, srs, rl):
        self.mappings.append([drs, srs, rl])

    def __getitem__(self, item):
        for mapping in self.mappings:
            drs = mapping[0]
            srs = mapping[1]
            rl = mapping[2]
            if srs <= item < srs + rl:
                return drs + item - srs
        return item

    def map_ranges(self, ranges):
        new_ranges = []
        while ranges:
            curr_range = ranges.pop()
            cr1 = curr_range[0]
            cr2 = cr1 + curr_range[1] - 1
            no_hit = True
            for mapping in self.mappings:
                drs = mapping[0]
                srs = mapping[1]
                rl = mapping[2]
                s1 = srs
                s2 = srs + rl - 1
                if s1 < cr1 and s2 == cr1:
                    ranges.append([s2 + 1, cr2 - s2])
                    new_ranges.append([drs + rl - 1, 1])
                    no_hit = False
                elif s1 < cr1 and cr1 < s2 < cr2:
                    ranges.append([s2 + 1, cr2 - s2])
                    new_ranges.append([drs + cr1 - s1, s2 - cr1 + 1])
                    no_hit = False
                elif s1 < cr1 and s2 >= cr2:
                    new_ranges.append([drs + cr1 - s1, cr2-cr1+1])
                    no_hit = False
                elif s1 == cr1 and s2 == cr1:
                    new_ranges.append([drs, 1])
                elif s1 == cr1 and cr1 < s2 < cr2:
                    ranges.append([s2 + 1, cr2 - s2])
                    new_ranges.append([drs, s2 - cr1 + 1])
                    no_hit = False
                elif s1 == cr1 and s2 >= cr2:
                    new_ranges.append([drs, cr2-cr1+1])
                    no_hit = False
                elif cr1 < s1 < cr2 and cr1 < s2 < cr2:
                    ranges.append([cr1, s1 - cr1])
                    ranges.append([s2 + 1, cr2 - s2])
                    new_ranges.append([drs, rl])
                    no_hit = False
                elif cr1 < s1 < cr2 and s2 >= cr2:
                    ranges.append([cr1, s1 - cr1])
                    new_ranges.append([drs, cr2-s1+1])
                elif s1 == cr2:
                    ranges.append([cr1, s1 - cr1])
                    new_ranges.append([drs, 1])
            if no_hit:
                new_ranges.append(curr_range)

        return new_ranges


def solve(puzzle_input):
    seeds = []
    seed_to_soil_map = KeyDefaultDict()
    soil_to_fertilizer_map = KeyDefaultDict()
    fertilizer_to_water_map = KeyDefaultDict()
    water_to_light_map = KeyDefaultDict()
    light_to_temperature_map = KeyDefaultDict()
    temperature_to_humidity_map = KeyDefaultDict()
    humidity_to_location_map = KeyDefaultDict()

    current_map = None
    for line in puzzle_input:
        if not line:
            continue
        elif line.startswith("seeds: "):
            seeds = [int(n) for n in line.replace("seeds: ", "").split(" ")]
        elif line == "seed-to-soil map:":
            current_map = seed_to_soil_map
        elif line == "soil-to-fertilizer map:":
            current_map = soil_to_fertilizer_map
        elif line == "fertilizer-to-water map:":
            current_map = fertilizer_to_water_map
        elif line == "water-to-light map:":
            current_map = water_to_light_map
        elif line == "light-to-temperature map:":
            current_map = light_to_temperature_map
        elif line == "temperature-to-humidity map:":
            current_map = temperature_to_humidity_map
        elif line == "humidity-to-location map:":
            current_map = humidity_to_location_map
        else:
            drs, srs, rl = [int(n) for n in line.split(" ")]
            current_map.add_mapping(drs, srs, rl)

    locations1 = []
    for seed in seeds:
        soil = seed_to_soil_map[seed]
        fertilizer = soil_to_fertilizer_map[soil]
        water = fertilizer_to_water_map[fertilizer]
        light = water_to_light_map[water]
        temperature = light_to_temperature_map[light]
        humidity = temperature_to_humidity_map[temperature]
        location = humidity_to_location_map[humidity]

        locations1.append(location)

    min_location = None
    for i in range(0, int(len(seeds) / 2)):
        seed_start = seeds[2 * i]
        seed_len = seeds[2 * i + 1]

        ranges = [[seed_start, seed_len]]
        ranges = seed_to_soil_map.map_ranges(ranges)
        ranges = soil_to_fertilizer_map.map_ranges(ranges)
        ranges = fertilizer_to_water_map.map_ranges(ranges)
        ranges = water_to_light_map.map_ranges(ranges)
        ranges = light_to_temperature_map.map_ranges(ranges)
        ranges = temperature_to_humidity_map.map_ranges(ranges)
        ranges = humidity_to_location_map.map_ranges(ranges)

        for the_range in ranges:
            min_location = min(the_range[0], min_location) if min_location else the_range[0]

    return min(locations1), min_location


def main():
    test_input_file = "input/" + os.path.basename(__file__).replace("aoc", "testinput").replace("py", "txt")
    test_input_file2 = test_input_file.replace(".txt", "-2.txt")
    if os.path.isfile(test_input_file):
        start = time.time()
        with open(test_input_file) as f:
            content1 = f.read().splitlines()
        if os.path.isfile(test_input_file2):
            with open(test_input_file2) as f:
                content2 = f.read().splitlines()
            solution1, _ = solve(content1)
            _, solution2 = solve(content2)
        else:
            solution1, solution2 = solve(content1)
        if solution1 != TEST_SOLUTION1:
            print(f"TEST solution 1 '{solution1}' not correct!")
            return
        if solution2 != TEST_SOLUTION2:
            print(f"TEST solution 2 '{solution2}' not correct!")
            return
        end = time.time()
        print_diff(end - start, True)
    else:
        open(test_input_file, 'a').close()

    input_file = "input/" + os.path.basename(__file__).replace("aoc", "input").replace("py", "txt")
    if os.path.isfile(input_file):
        with open(input_file) as f:
            content = f.read().splitlines()
        start = time.time()
        solution1, solution2 = solve(content)
        print("Solution 1: {}".format(solution1))
        print("Solution 2: {}".format(solution2))
        end = time.time()
        print_diff(end - start, False)
    else:
        open(input_file, 'a').close()


def print_diff(diff, is_test):
    prefix = "TEST " if is_test else ""
    if diff >= 1:
        print("The {}solutions took {}s".format(prefix, round(diff)))
    else:
        print("The {}solutions took {}ms".format(prefix, round(diff * 1000)))


if __name__ == "__main__":
    main()
