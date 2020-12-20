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


def transpose_edge(edge, edge_length):
    new_edge = 0
    for index in range(edge_length):
        if edge & (1 << (edge_length - index - 1)):
            new_edge |= 1 << index

    return new_edge


def print_edges(edges):
    format = lambda edge: "{:.>10} {:>4}".format(
        bin(edge)[2:].replace("1", "#").replace("0", "."),
        edge,
    )

    print("t", format(edges[0]))
    print("r", format(edges[1]))
    print("b", format(edges[2]))
    print("l", format(edges[3]))


# loading and initialization

tiles_raw = open("day 20/input.txt").read().strip().split("\n\n")

tiles = dict()
for tile in tiles_raw:
    header, *data = tile.split("\n")
    _, tile_num = header[:-1].split()
    tile_num = int(tile_num)
    tiles[tile_num] = data

edge_length = 10

tiles_as_edges = dict()
for id, tile in tiles.items():
    tiles_as_edges[id] = make_edges(tiles[id], edge_length)


# find corner tiles

corner_tile_ids_multiplied = 1

for tile_id, tile_edges in tiles_as_edges.items():
    outer_edge_count = 0

    found_matching_edge = False
    for edge in tile_edges:
        edge_transposed = transpose_edge(edge, edge_length)

        for pair_id, pair_edges in tiles_as_edges.items():
            if pair_id == tile_id:
                continue

            if edge in pair_edges or edge_transposed in pair_edges:
                found_matching_edge = True
                break

        if found_matching_edge:
            found_matching_edge = False
        else:
            outer_edge_count += 1

    if outer_edge_count == 2:
        # this is a corner tile
        corner_tile_ids_multiplied *= tile_id

print(f"Corner tile IDs multiplied: {corner_tile_ids_multiplied}")