file = open("day 3/input.txt")

slope_map = [line.rstrip() for line in file.readlines()]
slope_map_width = len(slope_map[0])

slope_x = 3
slope_y = 1

pos_x = 0
pos_y = 0

tree_count = 0

while pos_y < len(slope_map):
    if slope_map[pos_y][pos_x] == "#":
        tree_count += 1

    pos_x += slope_x
    pos_y += slope_y

    pos_x %= slope_map_width


print(f"Solution: {tree_count}")