import copy


def count_adjecent(seats, x, y):
    positions = [
        # top row
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        # right seat
        (x + 1, y),
        # bottom row
        (x + 1, y + 1),
        (x, y + 1),
        (x - 1, y + 1),
        # left seat
        (x - 1, y),
    ]

    count = 0
    for x, y in positions:
        if 0 <= x < len(seats[0]) and 0 <= y < len(seats):
            if seats[y][x] == "#":
                count += 1

    return count


def step(seats):
    new_seats = copy.deepcopy(seats)
    stable = True

    for y in range(len(seats)):
        for x in range(len(seats[0])):
            seat = seats[y][x]
            count = count_adjecent(seats, x, y)

            # rule 1
            if seat == "L" and count == 0:
                seat = "#"
                stable = False
            # rule 2
            elif seat == "#" and count >= 4:
                seat = "L"
                stable = False
            # rule 3
            else:
                pass

            new_seats[y][x] = seat

    return new_seats, stable


def count_occupied(seats):
    return sum([row.count("#") for row in seats])


def print_seats(seats):
    for row in seats:
        for s in row:
            print(s, end="")
        print()


seats = [list(s.rstrip()) for s in open("day 11/input.txt").readlines()]
stable = False

# print_seats(seats)
# print("---")

while not stable:
    seats, stable = step(seats)
    # print_seats(seats)
    # print("---")

print_seats(seats)

occupied_seats = count_occupied(seats)

print(f"Occupied seats: {occupied_seats}")