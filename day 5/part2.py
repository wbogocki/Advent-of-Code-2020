file = open("day 5/input.txt")

boarding_passes = [bp for bp in file.readlines()]


def seat_coordinates(boarding_pass):
    seat_row_min = 0
    seat_row_max = 127

    for half in boarding_pass[:7]:
        rows = seat_row_max - seat_row_min + 1
        if half == "F":
            seat_row_max -= (int)(rows / 2)
        else:
            seat_row_min += (int)(rows / 2)

    if half == "F":
        seat_row = seat_row_min
    else:
        seat_row = seat_row_max

    seat_column_min = 0
    seat_column_max = 7

    for half in boarding_pass[7:11]:
        columns = seat_column_max - seat_column_min + 1
        if half == "L":
            seat_column_max -= (int)(columns / 2)
        else:
            seat_column_min += (int)(columns / 2)

    if half == "L":
        seat_column = seat_column_min
    else:
        seat_column = seat_column_max

    return seat_row, seat_column


def seat_id(row, column):
    return row * 8 + column


seats = set()

for boarding_pass in boarding_passes:
    row, column = seat_coordinates(boarding_pass)
    id = seat_id(row, column)
    seats.add(id)


my_seat = None

for seat in seats:
    if seat + 1 not in seats:
        my_seat = seat + 1
        break

print(f"My seat ID: {my_seat}")