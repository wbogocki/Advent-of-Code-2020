instructions = [
    (line[0], int(line[1:])) for line in open("day 12/input.txt").readlines()
]

directions = {
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
    "N": (0, 1),
}

rotations = {
    "E": ["E", "S", "W", "N"],
    "S": ["S", "W", "N", "E"],
    "W": ["W", "N", "E", "S"],
    "N": ["N", "E", "S", "W"],
}

facing = "E"
x, y = 0, 0

for (action, parameter) in instructions:
    if action == "N":
        y += parameter
    if action == "S":
        y -= parameter
    if action == "E":
        x += parameter
    if action == "W":
        x -= parameter

    if action == "L":
        facing = rotations[facing][int(-parameter / 90)]
    if action == "R":
        facing = rotations[facing][int(parameter / 90)]

    if action == "F":
        (dx, dy) = directions[facing]
        x += dx * parameter
        y += dy * parameter

    print(f"({facing} {x} {y}) {action} {parameter}")

manhattan_distance = abs(x) + abs(y)

print(f"Manhattan distance: {manhattan_distance}")