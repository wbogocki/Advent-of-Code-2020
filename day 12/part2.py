instructions = [
    (line[0], int(line[1:])) for line in open("day 12/input.txt").readlines()
]

directions = {
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
    "N": (0, 1),
}

ship_x, ship_y = 0, 0
waypoint_x, waypoint_y = 10, 1


def rotate(point, angle):
    x, y = point
    if angle == 90:
        return (y, -x)
    if angle == 180:
        return (-x, -y)
    if angle == 270:
        return (-y, x)


for (action, parameter) in instructions:
    if action == "N":
        waypoint_y += parameter
    if action == "S":
        waypoint_y -= parameter
    if action == "E":
        waypoint_x += parameter
    if action == "W":
        waypoint_x -= parameter

    if action == "L":
        waypoint_x, waypoint_y = rotate((waypoint_x, waypoint_y), 360 - parameter)
    if action == "R":
        waypoint_x, waypoint_y = rotate((waypoint_x, waypoint_y), parameter)

    if action == "F":
        ship_x += waypoint_x * parameter
        ship_y += waypoint_y * parameter

    print(f"(s {ship_x} {ship_y}) (w {waypoint_x} {waypoint_y}) {action} {parameter}")

manhattan_distance = abs(ship_x) + abs(ship_y)

print(f"Manhattan distance: {manhattan_distance}")
