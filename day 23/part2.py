from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Cup:
    label: int
    next: Cup


# load cups

cups = [int(cup) for cup in open("day 23/input.txt").read().rstrip()]

min_cup_label = min(cups)
max_cup_label = max(cups)

cups += [label for label in range(max_cup_label + 1, 1_000_000 + 1)]
max_cup_label = 1_000_000

# build the list of cups

first_cup = Cup(cups[0], None)
current_cup = first_cup

lookup = dict()
lookup[cups[0]] = first_cup

for cup_label in cups[1:]:
    cup = Cup(cup_label, None)
    current_cup.next = cup
    current_cup = current_cup.next
    lookup[cup_label] = cup
    if cup_label % 100_000 == 0:
        print(cup_label)
current_cup.next = first_cup
current_cup = first_cup

print("Generated cups linked list")


# simulate the game

for move_number in range(1, 10_000_000 + 1):
    # print(f"-- move {move_number} --")
    # print(f"current: {current_cup.label}")
    # print(f"cups: ", end="")

    # print_cup = first_cup
    # while print_cup.next != first_cup:
    #     print(f"{print_cup.label} ", end="")
    #     print_cup = print_cup.next
    # print(print_cup.label)

    # pick up cups

    picked_up_cups = [
        current_cup.next,
        current_cup.next.next,
        current_cup.next.next.next,
    ]

    current_cup.next = picked_up_cups[-1].next  # detach the three cups

    picked_up_cups_labels = [cup.label for cup in picked_up_cups]

    # print(f"picked up: {picked_up_cups_labels}")

    # destination cup

    destination_cup_label = current_cup.label - 1

    if destination_cup_label < min_cup_label:
        destination_cup_label = max_cup_label
    while destination_cup_label in picked_up_cups_labels:
        destination_cup_label -= 1
        if destination_cup_label < min_cup_label:
            destination_cup_label = max_cup_label

    # print(f"destination cup: {destination_cup_label}")

    # put the picked up cups after the destination cup

    destination_cup = lookup[destination_cup_label]

    picked_up_cups[-1].next = destination_cup.next
    destination_cup.next = picked_up_cups[0]

    # advance current cup

    current_cup = current_cup.next

    # input()

    if move_number % 100_000 == 0:
        print(move_number)

print("Simulated the game")


# get the two cups after cup 1 and multiply their

first_cup = lookup[1]
cup_1_plus_1 = first_cup.next.label
cup_1_plus_2 = first_cup.next.next.label

print(cup_1_plus_1)
print(cup_1_plus_2)

print(f"Solution: {cup_1_plus_1 * cup_1_plus_2}")