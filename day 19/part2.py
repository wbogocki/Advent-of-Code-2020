from dataclasses import dataclass
from pprint import pprint
import itertools


@dataclass
class ASTNode:
    value: str
    children: list


def resolve_rules(rules):
    unresolved_rules = rules.copy()

    resolved_rules = dict()

    for name in list(unresolved_rules):
        if rules[name] in ["a", "b"]:
            resolved_rules[name] = unresolved_rules.pop(name)

    while unresolved_rules:
        resolved_now = list()

        for name, body in unresolved_rules.items():
            resolved = True

            new_body = []
            for token in body.split():
                if token in ["a", "b", "|", "(", ")"]:
                    new_body.append(token)
                    continue
                elif token in resolved_rules:
                    if len(resolved_rules[token].split()) > 1:
                        new_body.append(f"( {resolved_rules[token]} )")
                    else:
                        new_body.append(resolved_rules[token])
                else:
                    new_body.append(token)
                    resolved = False

            unresolved_rules[name] = " ".join(new_body)

            if resolved:
                # print(f"Resolved rule {name}")
                resolved_now.append(name)

        for name in resolved_now:
            resolved_rules[name] = unresolved_rules.pop(name)

    for name in resolved_rules:
        # insert implicit pluses

        resolved_rules[name] = resolved_rules[name].replace("a b", "a + b")
        resolved_rules[name] = resolved_rules[name].replace("b a", "b + a")
        resolved_rules[name] = resolved_rules[name].replace("a a", "a + a")
        resolved_rules[name] = resolved_rules[name].replace("b b", "b + b")
        resolved_rules[name] = resolved_rules[name].replace(") (", ") + (")
        resolved_rules[name] = resolved_rules[name].replace("a (", "a + (")
        resolved_rules[name] = resolved_rules[name].replace("b (", "b + (")
        resolved_rules[name] = resolved_rules[name].replace(") a", ") + a")
        resolved_rules[name] = resolved_rules[name].replace(") b", ") + b")

    return resolved_rules


def parse_rule(rule):
    # Shunting-yard
    precedence = {
        "(": 3,
        ")": 3,
        "+": 2,
        "|": 1,
    }
    output_queue = []
    operator_stack = []
    for token in rule.split():
        if token in ["+", "|"]:
            while (
                operator_stack
                and precedence[operator_stack[-1]] >= precedence[token]
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
            output_queue.append(token)

    while operator_stack:
        output_queue.append(operator_stack.pop())

    # AST
    ast = []
    for it in output_queue:
        if it in ["+", "|"]:
            a = ast.pop()
            b = ast.pop()
            ast.append(ASTNode(it, [b, a]))
        else:
            ast.append(ASTNode(it, []))

    return ast.pop()


def print_ast(node, indent=0):
    print(" " * indent, node.value)
    for child in node.children:
        print_ast(child, indent=indent + 2)


def print_ast_as_expression(node, root=True):
    if node.value[0] in ["a", "b"]:
        print(node.value, end="")

    elif node.value in ["+", "|"]:
        print("(", end="")
        for index, child in enumerate(node.children):
            print_ast_as_expression(child, root=False)
            if index != len(node.children) - 1:
                print(node.value, end="")
        print(")", end="")

    if root:
        print()


def match_ast_inner(text, node):
    # print(f"matching {text} against node {node.value}")
    # print_ast(node)
    # input()

    if node.value == "+":
        length = 0
        for child in node.children:
            child_length = match_ast_inner(text[length:], child)
            if child_length is None:
                return None
            else:
                length += child_length

        return length

    elif node.value == "|":
        for child in node.children:
            length = match_ast_inner(text, child)
            if length is not None:
                return length

        return None

    else:
        if text.startswith(node.value):
            return len(node.value)
        else:
            return None


def match_ast(text, node):
    return match_ast_inner(text, node) == len(text)


# def generate_rule_8(depth):
#     # depth = how many levels of recursion should be allowed
#     rule_8 = "42 | 42 8"
#     for _ in range(depth):
#         rule_8 = rule_8.replace("8", f"( {rule_8} )")
#     return rule_8.replace("8", "42")


# def generate_rule_11(depth):
#     # depth = how many levels of recursion should be allowed
#     rule_11 = "42 31 | 42 11 31"
#     for _ in range(depth):
#         rule_11 = rule_11.replace("11", f"( {rule_11} )")
#     return rule_11.replace("11", "( 42 31 )")


# the length that matches this ast. Assumes same length for all branches.
def pattern_length(ast):
    if ast.value == "+":
        length = 0
        for child in ast.children:
            length += pattern_length(child)
        return length
    elif ast.value == "|":
        return pattern_length(ast.children[0])
    else:
        return 1


def match_8_11(text, resolved_rules):
    # rule 8: 42 | 42 8
    # rule 11: 42 31 | 42 11 31

    # rules 8 and 11 simplify to 42 n times followd by 42 k times followed by 31 k times
    asts = dict()
    for name in ["42", "31"]:
        asts[name] = parse_rule(resolved_rules[name])

    # input(message)

    length_42 = pattern_length(asts["42"])
    length_31 = pattern_length(asts["31"])

    # let's assume the lenghts are the same to partition the text more easily
    assert length_42 == length_31
    chunk_length = length_42

    chunks = len(text) / chunk_length
    assert chunks.is_integer()
    chunks = int(chunks)

    # create possible ways (distributions) the rules could match this text
    distributions = []
    k = 1
    while k * 2 < chunks:
        distribution = list(
            itertools.chain(
                itertools.repeat("42", chunks - k),
                itertools.repeat("31", k),
            )
        )
        distributions.append(distribution)
        k += 1

    # print(text)
    # pprint(distributions)
    # input()

    for distribution in distributions:
        offset = 0
        for rule_name in distribution:
            chunk = message[offset : offset + chunk_length]
            if match_ast(chunk, asts[rule_name]):
                # print(f"matched {rule_name} with {chunk}")
                offset += chunk_length
            else:
                break

        if offset == len(text):
            return True

    return False


# load input file

rules_text, messages_text = open("day 19/input.txt").read().split("\n\n")

# load rules

rules = dict()

for rule in rules_text.splitlines():
    name, body = rule.split(":")
    body = body.lstrip()

    if body[0] == '"':
        rules[name] = body[1]
    else:
        rules[name] = body

# resolved rules

resolved_rules = resolve_rules(rules)

# load messages

messages = messages_text.splitlines()

# match

matches = set()

for message in messages:
    if match_8_11(message, resolved_rules):
        matches.add(message)

for message in matches:
    print(message)

print(f"Messages matching rule 0: {len(matches)}")