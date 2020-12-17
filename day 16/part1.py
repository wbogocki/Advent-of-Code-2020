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


def get_invalid_fields(rules, ticket):
    # check if field fulfills to any rule
    for field in ticket:
        field_ok = False

        # check if rule is fulfilled
        for _, ranges in rules.items():
            rule_ok = False

            # check if one of the ranges is correct
            for (low, high) in ranges:
                if low <= field <= high:
                    rule_ok = True
                    break

            if rule_ok:
                field_ok = True
                break

        if not field_ok:
            yield field

    return None


rules, my_ticket, nearby_tickets = open("day 16/input.txt").read().split("\n\n")

rules = parse_rules(rules)
my_ticket = parse_tickets(my_ticket)[0]
nearby_tickets = parse_tickets(nearby_tickets)

scanning_error_rate = 0

for ticket in nearby_tickets:
    for field in get_invalid_fields(rules, ticket):
        scanning_error_rate += field

print(f"Scanning error rate: {scanning_error_rate}")