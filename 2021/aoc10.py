with open("input/input10.txt") as f:
    content = f.read().splitlines()

lines = content

pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


def get_first_illegal_character(the_line):
    the_stack = []
    for char in list(the_line):
        if char in [")", "]", "}", ">"]:
            latest_char = the_stack.pop()
            if latest_char not in pairs or pairs[latest_char] != char:
                return char
        else:
            the_stack.append(char)

    return None


def get_score(the_char):
    if the_char == ")":
        return 3
    elif the_char == "]":
        return 57
    elif the_char == "}":
        return 1197
    elif the_char == ">":
        return 25137
    else:
        raise Exception("You cannot be serious!")


syntax_error_score = 0
incomplete_lines = []
for line in lines:
    illegal_character = get_first_illegal_character(line)
    if illegal_character:
        syntax_error_score += get_score(illegal_character)
    else:
        incomplete_lines.append(line)

print("Solution 1: the total syntax error score for those errors is {}".format(syntax_error_score))


def fix_line(the_line):
    the_completions = []

    the_stack = []
    for char in list(the_line):
        if char in [")", "]", "}", ">"]:
            latest_char = the_stack.pop()
            if latest_char not in pairs or pairs[latest_char] != char:
                raise Exception("You cannot be serious!")
        else:
            the_stack.append(char)

    for remainder in the_stack:
        if remainder in pairs:
            the_completions.insert(0, pairs[remainder])
        else:
            raise Exception("You cannot be serious!")

    return the_completions


def get_completion_score(the_completions):
    the_score = 0
    for the_char in the_completions:
        the_score *= 5
        if the_char == ")":
            the_score += 1
        elif the_char == "]":
            the_score += 2
        elif the_char == "}":
            the_score += 3
        elif the_char == ">":
            the_score += 4
        else:
            raise Exception("You cannot be serious!")
    return the_score


scores = []
for line in incomplete_lines:
    completions = fix_line(line)
    scores.append(get_completion_score(completions))
scores.sort()

middle_score = scores[int((len(scores) - 1) / 2)]

print("Solution 2: the middle score is {}".format(middle_score))
