def tokenize_expr(expr):
    tokens = []

    token = ""
    for char in expr:
        if char == " ":
            if token:
                tokens.append(token)
                token = ""
        elif char in ["+", "*", "(", ")"]:
            if token:
                tokens.append(token)
                token = ""

            tokens.append(char)
        else:
            token += char

    if token:
        tokens.append(token)

    return tokens


def compute_expr(expr_tokens):
    VALUE = 0
    OPERATION = 1

    stack = [[0, "+"]]

    for token in expr_tokens:
        if token == "+":
            stack[-1][OPERATION] = "+"

        elif token == "*":
            stack[-1][OPERATION] = "*"

        elif token == "(":
            stack.append([0, "+"])

        elif token == ")":
            value, _ = stack.pop()

            op = stack[-1][OPERATION]
            if op == "+":
                stack[-1][VALUE] += value
            else:
                stack[-1][VALUE] *= value

        else:
            op = stack[-1][OPERATION]
            if op == "+":
                stack[-1][VALUE] += int(token)
            else:
                stack[-1][VALUE] *= int(token)

    value, _ = stack.pop()

    return value


expressions = [expr.strip() for expr in open("day 18/input.txt").readlines()]

sum_of_values = 0

for expr in expressions:
    tokens = tokenize_expr(expr)
    value = compute_expr(tokens)
    sum_of_values += value

print(f"Sum of values: {sum_of_values}")