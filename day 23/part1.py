cups = [int(cup) for cup in open("day 23/input.txt").read().rstrip()]

min_cup_label = min(cups)
max_cup_label = max(cups)

print(min_cup_label)
print(max_cup_label)

current_cup_index = 0

for move_number in range(1, 101):
    print(f"-- move {move_number} --")
    print(f"current: {current_cup_index}")
    print(f"cups: {cups}")

    current_cup_label = cups[current_cup_index]

    # rotate cups

    rotate_around_index = cups.index(current_cup_label)
    # print(rotate_around_index)
    # print(cups)
    cups = cups[rotate_around_index:] + cups[:rotate_around_index]
    # print(cups)

    picked_up_cups = [cups.pop(1), cups.pop(1), cups.pop(1)]

    print(f"picked up: {picked_up_cups}")

    destination_cup_label = current_cup_label - 1
    if destination_cup_label < min_cup_label:
        destination_cup_label = max_cup_label
    while destination_cup_label in picked_up_cups:
        destination_cup_label -= 1
        if destination_cup_label < min_cup_label:
            destination_cup_label = max_cup_label

    destination_cup_index = cups.index(destination_cup_label)

    print(f"destination cup: {destination_cup_label}")

    if destination_cup_index == len(cups) - 1:
        # special case: add picked up cups at the end of the cups list,
        # if we didn't have this, we would wrap around and add to the front
        cups.extend(picked_up_cups)
    else:
        cups = (
            cups[: destination_cup_index + 1]
            + picked_up_cups
            + cups[destination_cup_index + 1 :]
        )

    # rotate cups back
    # print(cups)
    cups = cups[-current_cup_index:] + cups[:-current_cup_index]
    # print(cups)

    assert current_cup_label == cups[current_cup_index]

    current_cup_index = (current_cup_index + 1) % len(cups)

    # input()
    print()


index_of_1 = cups.index(1)

print("Final cup labels: ", end="")
for offset in range(len(cups) - 1):
    print(cups[(index_of_1 + offset + 1) % len(cups)], end="")
print()