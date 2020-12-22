p1_deck, p2_deck = [
    [int(card) for card in deck.splitlines()[1:]]
    for deck in open("day 22/input.txt").read().split("\n\n")
]


def round(p1_deck, p2_deck):
    p1_card = p1_deck.pop(0)
    p2_card = p2_deck.pop(0)

    if p1_card > p2_card:
        p1_deck.append(p1_card)
        p1_deck.append(p2_card)
    else:
        p2_deck.append(p2_card)
        p2_deck.append(p1_card)


while p1_deck and p2_deck:
    round(p1_deck, p2_deck)

    print("-- Round --")
    print(f"P1: {p1_deck}")
    print(f"P2: {p2_deck}")
    print()


winning_deck = p1_deck or p2_deck

print(f"Winning Deck: {winning_deck}")


score = 0
for it in range(1, len(winning_deck) + 1):
    score += winning_deck[-it] * it

print(f"Score:  {score}")