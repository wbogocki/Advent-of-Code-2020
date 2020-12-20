import itertools
from pprint import pprint

X = 0
Y = 1
TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


def make_edges(tile, edge_length):
    # top
    top = 0
    for index in range(edge_length):
        terrain = tile[0][index]
        if terrain == "#":
            top |= 1 << (edge_length - index - 1)

    # right
    right = 0
    for index in range(edge_length):
        terrain = tile[index][-1]
        if terrain == "#":
            right |= 1 << (edge_length - index - 1)

    # bottom
    bottom = 0
    for index in range(edge_length):
        terrain = tile[-1][index]
        if terrain == "#":
            bottom |= 1 << (edge_length - index - 1)

    # left
    left = 0
    for index in range(edge_length):
        terrain = tile[index][0]
        if terrain == "#":
            left |= 1 << (edge_length - index - 1)

    return [top, right, bottom, left]


def print_edges(edges):
    format = lambda edge: "{:.>10} {:>4}".format(
        bin(edge)[2:].replace("1", "#").replace("0", "."),
        edge,
    )

    print("t", format(edges[0]))
    print("r", format(edges[1]))
    print("b", format(edges[2]))
    print("l", format(edges[3]))


def print_tile(tile):
    for row in tile:
        for col in row:
            print(col, end="")
        print()


def rotate_tile(tile):
    new_tile = []

    for x in range(len(tile[0])):
        new_row = ""
        for y in range(len(tile)):
            new_row += tile[len(tile) - y - 1][x]

        new_tile.append(new_row)

    return new_tile


def flip_tile_x(tile):
    new_tile = []

    for y in range(len(tile)):
        new_row = ""
        for x in range(len(tile[0])):
            new_row += tile[y][len(tile[0]) - x - 1]

        new_tile.append(new_row)

    return new_tile


def flip_tile_y(tile):
    new_tile = []

    for y in range(len(tile)):
        new_row = ""
        for x in range(len(tile[0])):
            new_row += tile[len(tile) - y - 1][x]

        new_tile.append(new_row)

    return new_tile


def iter_tile_rotations(tile):
    tile = tile.copy()
    yield tile
    for _ in range(3):
        tile = rotate_tile(tile)
        yield tile


def iter_tile_rotations_and_flips(tile):
    for t in iter_tile_rotations(tile):
        yield t

    flipped_x = flip_tile_x(tile)
    for t in iter_tile_rotations(flipped_x):
        yield t

    flipped_y = flip_tile_y(tile)
    for t in iter_tile_rotations(flipped_y):
        yield t

    flipped_xy = flip_tile_y(flipped_x)
    for t in iter_tile_rotations(flipped_xy):
        yield t


def print_tiles(tiles, tile_positions, min_position, max_position, edge_length):
    for pos_y in range(min_position[Y], max_position[Y] + 1):
        for subpos_y in range(edge_length):
            for pos_x in range(min_position[X], max_position[X] + 1):
                for tile_id, tile_data in tiles.items():
                    tile_position = tile_positions[tile_id]
                    if pos_x == tile_position[X] and pos_y == tile_position[Y]:
                        print(tile_data[subpos_y], end=" ")

            print()

        print()


def assemble_image(tiles, tile_positions, min_position, max_position, edge_length):
    image = ""

    for pos_y in range(min_position[Y], max_position[Y] + 1):
        for subpos_y in range(edge_length):
            # skip top and bottom borders
            if subpos_y == 0 or subpos_y == edge_length - 1:
                continue

            for pos_x in range(min_position[X], max_position[X] + 1):
                for tile_id, tile_data in tiles.items():
                    tile_position = tile_positions[tile_id]
                    if pos_x == tile_position[X] and pos_y == tile_position[Y]:
                        # print without left and right border
                        image += tile_data[subpos_y][1:-1]

            image += "\n"

    return image


# loading and initialization

tiles_raw = open("day 20/input.txt").read().strip().split("\n\n")

tiles = dict()
for tile in tiles_raw:
    header, *data = tile.split("\n")
    _, tile_num = header[:-1].split()
    tile_num = int(tile_num)
    tiles[tile_num] = data

edge_length = 10


# arrange the tiles

anchor_tile_id = next(iter(tiles.keys()))

arranged_tiles = {
    anchor_tile_id: tiles[anchor_tile_id],
}

tile_positions = {
    anchor_tile_id: [0, 0],
}

min_position = [0, 0]
max_position = [0, 0]

while len(arranged_tiles) != len(tiles):
    # pprint(arranged_tiles.keys())
    # input()

    new_arranged_tiles = dict()

    for it_id, it_body in arranged_tiles.items():
        it_edges = make_edges(it_body, edge_length)

        for pair_id, ref_pair_body in tiles.items():
            if pair_id in arranged_tiles:
                continue

            for pair_body in iter_tile_rotations_and_flips(ref_pair_body):
                pair_edges = make_edges(pair_body, edge_length)

                if it_edges[TOP] == pair_edges[BOTTOM]:
                    new_arranged_tiles[pair_id] = pair_body
                    tile_positions[pair_id] = tile_positions[it_id].copy()
                    tile_positions[pair_id][Y] -= 1
                    min_position[Y] = min(min_position[Y], tile_positions[pair_id][Y])
                    break

                elif it_edges[RIGHT] == pair_edges[LEFT]:
                    new_arranged_tiles[pair_id] = pair_body
                    tile_positions[pair_id] = tile_positions[it_id].copy()
                    tile_positions[pair_id][X] += 1
                    max_position[X] = max(max_position[X], tile_positions[pair_id][X])
                    break

                elif it_edges[BOTTOM] == pair_edges[TOP]:
                    new_arranged_tiles[pair_id] = pair_body
                    tile_positions[pair_id] = tile_positions[it_id].copy()
                    tile_positions[pair_id][Y] += 1
                    max_position[Y] = max(max_position[Y], tile_positions[pair_id][Y])
                    break

                elif it_edges[LEFT] == pair_edges[RIGHT]:
                    new_arranged_tiles[pair_id] = pair_body
                    tile_positions[pair_id] = tile_positions[it_id].copy()
                    tile_positions[pair_id][X] -= 1
                    min_position[X] = min(min_position[X], tile_positions[pair_id][X])
                    break

    arranged_tiles.update(new_arranged_tiles)


# look for a sea monster

image = assemble_image(
    arranged_tiles,
    tile_positions,
    min_position,
    max_position,
    edge_length,
)

print(image)

image = [list(row) for row in image.split("\n")]

sea_monster_image = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]

for sea_monster in iter_tile_rotations_and_flips(sea_monster_image):
    # check every possible point on the image
    for y in range(len(image) - len(sea_monster)):
        for x in range(len(image[0]) - len(sea_monster[0])):
            found = True
            # match sea monster
            for sea_monster_y in range(len(sea_monster)):
                for sea_monster_x in range(len(sea_monster[0])):
                    image_y = y + sea_monster_y
                    image_x = x + sea_monster_x

                    sea_monster_flag = sea_monster[sea_monster_y][sea_monster_x] == "#"
                    image_flag = image[image_y][image_x] in ["#", "O"]

                    if sea_monster_flag and not image_flag:
                        found = False
                        break
                if not found:
                    break
            # draw the sea monster if found
            if found:
                for sea_monster_y in range(len(sea_monster)):
                    for sea_monster_x in range(len(sea_monster[0])):
                        image_y = y + sea_monster_y
                        image_x = x + sea_monster_x

                        if sea_monster[sea_monster_y][sea_monster_x] == "#":
                            image[image_y][image_x] = "O"


# reassemble the image string

image = "\n".join(["".join(row) for row in image])

print(image)

sea_monster_habitat_water_roughness = image.count("#")

print(f"Sea monster habitat water roughness: {sea_monster_habitat_water_roughness}")