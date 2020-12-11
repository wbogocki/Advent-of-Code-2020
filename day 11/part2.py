import copy


def count_visible(seats, x, y):
    directions = [
        # top row
        (-1, -1),
        (0, -1),
        (1, -1),
        # right seat
        (1, 0),
        # bottom row
        (1, 1),
        (0, 1),
        (-1, 1),
        # left seat
        (-1, 0),
    ]

    count = 0
    for dx, dy in directions:
        px = x + dx
        py = y + dy
        while 0 <= px < len(seats[0]) and 0 <= py < len(seats):
            if seats[py][px] == "#":
                count += 1
                break
            elif seats[py][px] == "L":
                break
            px += dx
            py += dy

    return count


def step(seats):
    new_seats = copy.deepcopy(seats)
    stable = True

    for y in range(len(seats)):
        for x in range(len(seats[0])):
            seat = seats[y][x]
            count = count_visible(seats, x, y)

            # rule 1
            if seat == "L" and count == 0:
                seat = "#"
                stable = False
            # rule 2
            elif seat == "#" and count >= 5:
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