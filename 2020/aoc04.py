import re

with open("input/input04.txt") as f:
    content = f.read().splitlines()

passports = [{}]
for line in content:
    if line:
        fields = line.split(" ") if " " in line else [line]
        for field in fields:
            key_value = field.split(":")
            passports[-1][key_value[0]] = key_value[1]
    else:
        passports.append({})


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


num_valid_passports1 = len(list(filter(validate_keys, passports)))
num_valid_passports2 = len(list(filter(validate_passport, passports)))

print("Solution 1: {} out of {} passports are valid".format(num_valid_passports1, len(passports)))
print("Solution 2: {} out of {} passports are valid".format(num_valid_passports2, len(passports)))
