file = open("day 3/input.txt")

slope_map = [line.rstrip() for line in file.readlines()]
slope_map_width = len(slope_map[0])


def count_trees(slope_x, slope_y):
    pos_x = 0
    pos_y = 0

    tree_count = 0

    while pos_y < len(slope_map):
        if slope_map[pos_y][pos_x] == "#":
            tree_count += 1

        pos_x += slope_x
        pos_y += slope_y

        pos_x %= slope_map_width

    return tree_count


count_1 = count_trees(1, 1)
count_2 = count_trees(3, 1)
count_3 = count_trees(5, 1)
count_4 = count_trees(7, 1)
count_5 = count_trees(1, 2)

solution = count_1 * count_2 * count_3 * count_4 * count_5

print(f"Solution: {solution}")