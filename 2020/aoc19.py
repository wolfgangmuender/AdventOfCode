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
        rule_id = int(rule_definition[0])
        rules[rule_id] = {
            "id": rule_id,
            "sub_rules": sub_rules,
            "value": value,
        }
    elif phase == 1:
        messages.append(line)
    else:
        raise Exception


def build_regex(rule, recursion_flag):
    if rule["value"]:
        return rule["value"]
    if rule["sub_rules"]:
        the_regex = ""
        curr_sub_rules = rule["sub_rules"]
        if len(curr_sub_rules) > 1:
            the_regex += '('
            regexes = []
            for curr_sub_rule in curr_sub_rules:
                sub_rule_regex = ""
                for part in curr_sub_rule:
                    sub_rule_regex += build_regex(rules[part], recursion_flag)
                regexes.append(sub_rule_regex)
            the_regex += "|".join(regexes)
            the_regex += ')'
        else:
            if recursion_flag and rule["id"] == 11:
                repetitons = []
                for i in range(1, 10):
                    regex_repetition = ""
                    for part in curr_sub_rules[0]:
                        regex_repetition += build_regex(rules[part], recursion_flag) + "{" + str(i) + "}"
                    repetitons.append(regex_repetition)
                the_regex = "(" + "|".join(repetitons) + ")"
            else:
                the_regex += "("
                for part in curr_sub_rules[0]:
                    the_regex += build_regex(rules[part], recursion_flag)
                the_regex += ")"
                if recursion_flag and rule["id"] == 8:
                    the_regex += "+"
        return the_regex


def find_matches_for_rule0(recursion_flag):
    rule_0_regex_str = "^" + build_regex(rules[0], recursion_flag) + "$"
    print(rule_0_regex_str)
    rule_0_regex = re.compile(rule_0_regex_str)

    matches = 0
    for message in messages:
        if rule_0_regex.match(message):
            matches += 1

    return matches


print("Solution 1: {} messages completely match rule 0".format(find_matches_for_rule0(False)))
print("Solution 2: {} messages completely match rule 0".format(find_matches_for_rule0(True)))
