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


def count_bags(bag):
    count = 1

    for inner_bag, inner_bag_count in rules[bag]:
        count += count_bags(inner_bag) * inner_bag_count

    return count


number_of_bags = count_bags("shiny gold") - 1

print(f"Number of bags: {number_of_bags}")
