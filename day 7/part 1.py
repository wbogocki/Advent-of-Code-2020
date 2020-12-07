file = open("day 7/input.txt")

text_rules = file.readlines()


def parse_contained_bag_text(bag_text):
    if bag_text == "no other bags":
        return None
    else:
        if bag_text.endswith(" bag"):
            bag_text = bag_text[:-4]
        elif bag_text.endswith(" bags"):
            bag_text = bag_text[:-5]
        else:
            raise Exception("Invalid contained bag text format!")

        quantity, color = bag_text.split(maxsplit=1)
        quantity = int(quantity)

        return color, quantity


def parse_text_rule(text_rule):
    [container, contained] = text_rule.split("contain")

    parsed_container = container[: -len(" bags ")]

    parsed_contained = []
    for bag_text in contained.strip().rstrip(".").split(","):
        bag = parse_contained_bag_text(bag_text)
        if bag:
            parsed_contained.append(bag)

    return parsed_container, parsed_contained


rules = dict([parse_text_rule(tr) for tr in text_rules])


def search(bag, path=[]):
    path = [*path, bag]

    for inner_bag, _ in rules[bag]:
        if inner_bag == "shiny gold":
            return path

        inner_path = search(inner_bag, path)
        if inner_path:
            return inner_path

    return None


found_in_bags = set()

for bag, _ in rules.items():
    if bag in found_in_bags:
        continue

    path = search(bag)
    if path:
        found_in_bags.update(path)


solution = len(found_in_bags)

print(f"Solution: {solution}")
