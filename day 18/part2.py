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


def precendence(operator):
    if operator == "+":
        return 2
    else:
        return 1


def compute_expr(expr_tokens):
    # Shunting-yard
    output_queue = []
    operator_stack = []
    for token in expr_tokens:
        if token in ["+", "*"]:
            while (
                operator_stack
                and precendence(operator_stack[-1]) >= precendence(token)
                and operator_stack[-1] != "("
            ):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            if operator_stack[-1] == "(":
                operator_stack.pop()
        else:
            output_queue.append(int(token))

    while operator_stack:
        output_queue.append(operator_stack.pop())

    # Evaluation
    stack = []
    for it in output_queue:
        if it == "+":
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)
        elif it == "*":
            a = stack.pop()
            b = stack.pop()
            stack.append(a * b)
        else:
            stack.append(it)

    return stack.pop()


expressions = [expr.strip() for expr in open("day 18/input.txt").readlines()]

sum_of_values = 0

for expr in expressions:
    tokens = tokenize_expr(expr)
    value = compute_expr(tokens)
    print(value)
    sum_of_values += value

print(f"Sum of values: {sum_of_values}")