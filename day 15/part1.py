init_numbers = [int(num) for num in open("day 15/input.txt").read().split(",")]

past_turns = dict()
for index, number in enumerate(init_numbers[:-1]):
    past_turns[number] = index + 1

last_number = init_numbers[-1]

turn = len(past_turns) + 1
while turn != 2020:
    if last_number not in past_turns:
        # it is spoken for the first time
        next_number = 0
    else:
        # it has been spoken before
        next_number = turn - past_turns[last_number]

    past_turns[last_number] = turn

    turn += 1
    last_number = next_number

    print(f"turn {turn}: {next_number}")

print(f"2020th number: {last_number}")