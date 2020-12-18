from functools import reduce

with open("input/input18.txt") as f:
    content = f.read().splitlines()

expressions = []
for expression in content:
    curr_line = []
    for part in expression:
        if not part or part == ' ':
            continue
        elif part in ['+', '*', '(', ')']:
            curr_line.append(part)
        else:
            curr_line.append(int(part))
    expressions.append(curr_line)


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


line_results = []
for expression in expressions:
    curr_result = []
    curr_operator = []

    curr_result.append(0)
    curr_operator.append(add)
    for part in expression:
        if part == '(':
            curr_result.append(0)
            curr_operator.append(add)
        elif part == '*':
            curr_operator.append(multiply)
        elif part == '+':
            curr_operator.append(add)
        elif part == ')':
            the_right = curr_result.pop()
            the_operator = curr_operator.pop()
            the_left = curr_result.pop()
            curr_result.append(the_operator(the_left, the_right))
        else:
            the_right = part
            the_operator = curr_operator.pop()
            the_left = curr_result.pop()
            curr_result.append(the_operator(the_left, the_right))

    line_results.append(curr_result.pop())

print("Solution 1: the sum of the resulting values is {}".format(sum(line_results)))


def eval_without_brackets(curr_expression):
    i = 0
    while i < len(curr_expression):
        if curr_expression[i] == '+':
            curr_expression.pop(i)
            curr_expression[i - 1] = curr_expression[i - 1] + curr_expression.pop(i)
            continue
        if curr_expression[i] == '*':
            curr_expression.pop(i)
            continue
        i += 1
    return reduce(lambda x, y: x * y, curr_expression)


def eval_with_brackets(curr_expression):
    calc_expression = []
    while curr_expression:
        curr = curr_expression.pop(0)
        if curr == '(':
            calc_expression.append(eval_with_brackets(curr_expression))
        elif curr == ')':
            break
        else:
            calc_expression.append(curr)
    return eval_without_brackets(calc_expression)


line_results = []
for expression in expressions:
    line_results.append(eval_with_brackets(expression))

print("Solution 2: the sum of the resulting values is {}".format(sum(line_results)))
