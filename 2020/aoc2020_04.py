import os
import re
import time

TEST_SOLUTION1 = 2
TEST_SOLUTION2 = 2


def solve(puzzle_input):
    passports = [{}]
    for line in puzzle_input:
        if line:
            fields = line.split(" ") if " " in line else [line]
            for field in fields:
                key_value = field.split(":")
                passports[-1][key_value[0]] = key_value[1]
        else:
            passports.append({})

    return len(list(filter(validate_keys, passports))), len(list(filter(validate_passport, passports)))


def validate_keys(passport):
    passport_fields = sorted(passport.keys())
    if 'cid' in passport_fields:
        passport_fields.remove('cid')
    return passport_fields == ['byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid']


def match_year(value, minimum, maximum):
    if re.compile("^[0-9]{4}$").match(value):
        if minimum <= int(value) <= maximum:
            return True
    return False


def match_height(value):
    if re.compile("^[0-9]+cm$").match(value):
        if 150 <= int(value[:-2]) <= 193:
            return True
    if re.compile("^[0-9]+in$").match(value):
        if 59 <= int(value[:-2]) <= 76:
            return True
    return False


def validate_passport(passport):
    if not validate_keys(passport):
        return False

    if not match_year(passport['byr'], 1920, 2002):
        return False
    if not match_year(passport['iyr'], 2010, 2020):
        return False
    if not match_year(passport['eyr'], 2020, 2030):
        return False
    if not match_height(passport['hgt']):
        return False
    if not re.compile("^#[0-9a-f]{6}$").match(passport['hcl']):
        return False
    if passport['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False
    if not re.compile("^[0-9]{9}$").match(passport['pid']):
        return False

    return True


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
