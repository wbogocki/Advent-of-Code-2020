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
                if token in ["a", "b", "|", "(", ")", "."]:
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
    if node.value[0] in ["a", "b", "."]:
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
            match = match_ast_inner(text[length:], child)
            if match is None:
                return None
            else:
                length += match

        return length

    elif node.value == "|":
        for child in node.children:
            match = match_ast_inner(text, child)
            if match is not None:
                return match

        return None

    else:
        if text.startswith(node.value):
            return 1
        else:
            return None


def match_ast(text, node):
    return match_ast_inner(text, node) == len(text)


def iter_rule_8(depth):
    # depth = how many levels of recursion should be allowed
    rule_8 = "42 | 42 8"
    for _ in range(depth):
        rule_8 = rule_8.replace("8", f"( {rule_8} )")
        yield rule_8.replace("8", "42")


def iter_rule_11(depth):
    # depth = how many levels of recursion should be allowed
    rule_11 = "42 31 | 42 11 31"
    for _ in range(depth):
        rule_11 = rule_11.replace("11", f"( {rule_11} )")
        yield rule_11.replace("11", "( 42 31 )")


#
#
#
# NOTES FOR TOMORROW:
#
# IF THE PATTERN MATCHES ANYTHING THAT HAPPENED EARLIER IN THE STRING, IT WILL WORK BECAUSE OF THE (A | A blahblahblah) nature of it
#
# If we know how long 42 is we can tell the length of A and split the string to it (and we do because that's the length of messages that used to be matched)
#
# This string is always rule 8 N times + rule 11 n times
#
# Rule 11 is always 42 31 long or 2x that because it's either 42 31 or a 42 42 31 31
#
#
#

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

# iterate over every possible variant of rule 8 and 11

matches = set()
depth = 10

for rule_8, rule_11 in itertools.product(iter_rule_8(depth), iter_rule_11(depth)):
    # print(rule_8, "\t\t\t", rule_11)

    rules["8"] = rule_8
    rules["11"] = rule_11

    # resolve rules

    resolved_rules = resolve_rules(rules)
    # pprint(rules)

    # load messages

    messages = messages_text.splitlines()
    # pprint(messages)

    # build ast

    ast = parse_rule(resolved_rules["0"])
    # print_ast(ast)
    # print_ast_as_expression(ast)

    for message in messages:
        match = match_ast(message, ast)
        if match:
            # print(message)
            matches.add(message)

    print(len(matches))

for message in matches:
    print(message)

print(f"Messages matching rule 0: {len(matches)}")