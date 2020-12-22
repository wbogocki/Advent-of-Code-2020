PLAYER_1 = 1
PLAYER_2 = 2


class Game:
    def __init__(self, game_num, p1_deck, p2_deck):
        assert p1_deck
        assert p2_deck

        self.game_num = game_num
        self.round_num = 0
        self.history = set()
        self.p1_deck = p1_deck
        self.p2_deck = p2_deck
        self.p1_card = None
        self.p2_card = None

    def draw_cards(self):
        # sanity
        assert self.p1_deck[0]
        assert self.p2_deck[0]
        assert not self.p1_card
        assert not self.p2_card

        self.p1_card = self.p1_deck.pop(0)
        self.p2_card = self.p2_deck.pop(0)

        # print(f"draw {self.p1_card} {self.p2_card}")

        assert self.p1_card
        assert self.p2_card

        if len(self.p1_deck) >= self.p1_card and len(self.p2_deck) >= self.p2_card:
            # recurse
            deck_1 = self.p1_deck[: self.p1_card].copy()
            deck_2 = self.p2_deck[: self.p2_card].copy()
            return Game(self.game_num + 1, deck_1, deck_2)

        return PLAYER_1 if self.p1_card > self.p2_card else PLAYER_2

    def return_cards(self, winner):
        # print(f"return {self.p1_card} {self.p2_card}")

        # sanity
        assert self.p1_card
        assert self.p2_card

        if winner == PLAYER_1:
            self.p1_deck.append(self.p1_card)
            self.p1_deck.append(self.p2_card)
        else:
            self.p2_deck.append(self.p2_card)
            self.p2_deck.append(self.p1_card)

        # sanity
        self.p1_card = None
        self.p2_card = None

        self.round_num += 1

        # print(f"\n-- Round {self.round_num} (Game {self.game_num}) --")
        # print(f"Player 1's deck: {self.p1_deck}")
        # print(f"Player 2's deck: {self.p2_deck}")

    def winner(self):
        if f"{self.p1_deck}+{self.p2_deck}" in self.history:
            return PLAYER_1

        self.history.add(f"{self.p1_deck}+{self.p2_deck}")

        return PLAYER_1 if not self.p2_deck else PLAYER_2 if not self.p1_deck else None

    def winning_deck(self):
        return self.p1_deck or self.p2_deck


p1_deck, p2_deck = [
    [int(card) for card in deck.splitlines()[1:]]
    for deck in open("day 22/input.txt").read().split("\n\n")
]

game_num = 2
games = [Game(1, p1_deck, p2_deck)]

while True:
    draw_result = games[-1].draw_cards()
    if isinstance(draw_result, Game):
        games.append(draw_result)
        continue

    games[-1].return_cards(draw_result)
    winner = games[-1].winner()
    if winner:
        if len(games) == 1:
            break
        else:
            games.pop()
            games[-1].return_cards(winner)


winning_deck = games[0].winning_deck()

# print(f"Winning Deck: {winning_deck}")

score = 0
for it in range(1, len(winning_deck) + 1):
    score += winning_deck[-it] * it

print(f"Score:  {score}")