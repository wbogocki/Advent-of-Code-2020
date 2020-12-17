def parse_rules(rules):
    parsed_rules = dict()
    for rule in rules.splitlines():
        name, text = rule.split(":")
        ranges = []
        for range_ in text.split("or"):
            low, high = range_.split("-")
            ranges.append((int(low), int(high)))
        parsed_rules[name] = ranges
    return parsed_rules


def parse_tickets(tickets):
    _label, fields_lists = tickets.split("\n", maxsplit=1)
    parsed_tickets = []
    for fields_list in fields_lists.split("\n"):
        fields = [int(field) for field in fields_list.split(",")]
        parsed_tickets.append(fields)
    return parsed_tickets


def check_rule(field, ranges):
    for (low, high) in ranges:
        if low <= field <= high:
            return True

    return False


def check_validity(rules, ticket):
    # check if field fulfills to any rule
    for field in ticket:
        field_ok = False

        # check if rule is fulfilled
        for _, ranges in rules.items():
            if check_rule(field, ranges):
                field_ok = True
                break

        if not field_ok:
            return False

    return True


def deduce_fields(rules, tickets):
    deductions = dict()

    ticket_count = len(tickets)
    field_count = len(tickets[0])

    for field_index in range(field_count):
        deductions[field_index] = set(rules.keys())

    for ticket_index in range(ticket_count):
        for field_index in range(field_count):
            invalid_rules = set()
            for rule_name in deductions[field_index]:
                field_value = tickets[ticket_index][field_index]
                rule_ranges = rules[rule_name]

                if not check_rule(field_value, rule_ranges):
                    invalid_rules.add(rule_name)

            deductions[field_index].difference_update(invalid_rules)

    # print(deductions)

    done = False
    while not done:
        deduced_rules = set()

        for deduction_rules in deductions.values():
            if len(deduction_rules) == 1:
                deduced_rules.update(deduction_rules)

        for field_index in deductions:
            deduction_rules_left = deductions[field_index].difference(deduced_rules)
            if deduction_rules_left != set():
                deductions[field_index] = deduction_rules_left

        # print(deduced_rules)
        # input()

        if len(deduced_rules) == field_count:
            done = True

    for field_index in range(field_count):
        deductions[field_index] = next(iter(deductions[field_index]))

    return deductions


rules, my_ticket, nearby_tickets = open("day 16/input.txt").read().split("\n\n")

rules = parse_rules(rules)
my_ticket = parse_tickets(my_ticket)[0]
nearby_tickets = parse_tickets(nearby_tickets)

valid_nearby_tickets = []

for ticket in nearby_tickets:
    if check_validity(rules, ticket):
        valid_nearby_tickets.append(ticket)

deductions = deduce_fields(rules, valid_nearby_tickets)

solution = 1
for field_index, rule_name in deductions.items():
    if rule_name.startswith("departure"):
        solution *= my_ticket[field_index]

print(f"Solution: {solution}")