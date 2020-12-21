import re

with open("input/input19.txt") as f:
    content = f.read().splitlines()


def split_and_strip(the_string, separator):
    return [part.strip() for part in the_string.split(separator)]


rules = {}
messages = []
phase = 0
for line in content:
    if not line:
        phase += 1
    elif phase == 0:
        rule_definition = split_and_strip(line, ':')
        if '"' in rule_definition[1]:
            sub_rules = None
            value = rule_definition[1][1]
        else:
            sub_rules = []
            for option in split_and_strip(rule_definition[1], '|'):
                sub_rules.append(list(map(lambda x: int(x), split_and_strip(option, ' '))))
            value = None
        rules[int(rule_definition[0])] = {
            "sub_rules": sub_rules,
            "value": value,
        }
    elif phase == 1:
        messages.append(line)
    else:
        raise Exception

print(rules)


def build_regex(rule):
    if rule["value"]:
        return rule["value"]
    if rule["sub_rules"]:
        the_regex = ""
        curr_sub_rules = rule["sub_rules"]
        if len(curr_sub_rules) > 1:
            the_regex += '('
            regexes = []
            for curr_sub_rule in curr_sub_rules:
                regexes.append("")
                for part in curr_sub_rule:
                    regexes[-1] += build_regex(rules[part])
            the_regex += "|".join(regexes)
            the_regex += ')'
        else:
            for part in curr_sub_rules[0]:
                the_regex += build_regex(rules[part])
        return the_regex


rule_0_regex = re.compile("^" + build_regex(rules[0]) + "$")

matches = 0
for message in messages:
    if rule_0_regex.match(message):
        matches += 1

print("Solution 1: {} messages completely match rule 0".format(matches))
print("Solution 2: {}".format(0))
