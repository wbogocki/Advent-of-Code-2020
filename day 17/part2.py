iter_neighbors__offsets = []
for offset_x in range(-1, 2):
    for offset_y in range(-1, 2):
        for offset_z in range(-1, 2):
            for offset_w in range(-1, 2):
                # skip the active_cube itself
                if offset_x == 0 and offset_y == 0 and offset_z == 0 and offset_w == 0:
                    continue
                iter_neighbors__offsets.append((offset_x, offset_y, offset_z, offset_w))


def iter_neighbors(cube):
    cube_x, cube_y, cube_z, cube_w = cube

    for offset_x, offset_y, offset_z, offset_w in iter_neighbors__offsets:
        x = offset_x + cube_x
        y = offset_y + cube_y
        z = offset_z + cube_z
        w = offset_w + cube_w

        yield x, y, z, w


def print_state(state, min_x, max_x, min_y, max_y, min_z, max_z, min_w, max_w):
    for w in range(min_w, max_w + 1):
        for z in range(min_z, max_z + 1):
            print(f"z={z}, w={w}")
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x + 1):
                    if (x, y, z, w) in state:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()
            print()


state = set()

min_x, max_x = 0, 0
min_y, max_y = 0, 0
min_z, max_z = 0, 0
min_w, max_w = 0, 0

for y, row in enumerate(open("day 17/input.txt").readlines()):
    for x, cube in enumerate(row):
        if cube == "#":
            state.add((x, y, 0, 0))
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

for cycle in range(6):
    # print(f"Cycle {cycle}:", end="\n\n")
    # print_state(state, min_x, max_x, min_y, max_y, min_z, max_z, min_w, max_w)
    # input()

    new_state = set()
    new_min_x, new_max_x = 0, 0
    new_min_y, new_max_y = 0, 0
    new_min_z, new_max_z = 0, 0
    new_min_w, new_max_w = 0, 0

    observe_set = set(state)  # cubes that need to be updated because they were observed
    updated_set = set()  # cubes that have been updated

    while len(observe_set) > 0:
        cube = observe_set.pop()

        if cube in updated_set:
            continue

        updated_set.add(cube)

        neighbor_count = 0
        for neighbor_cube in iter_neighbors(cube):
            if neighbor_cube in state:
                neighbor_count += 1

            if cube in state and neighbor_cube not in updated_set:
                observe_set.add(neighbor_cube)

        make_active = False
        if cube in state:
            if neighbor_count in [2, 3]:
                make_active = True
        else:
            if neighbor_count == 3:
                make_active = True

        if make_active:
            new_state.add(cube)

            x, y, z, w = cube
            new_min_x, new_max_x = min(new_min_x, x), max(new_max_x, x)
            new_min_y, new_max_y = min(new_min_y, y), max(new_max_y, y)
            new_min_z, new_max_z = min(new_min_z, z), max(new_max_z, z)
            new_min_w, new_max_w = min(new_min_w, w), max(new_max_w, w)

    state = new_state
    min_x, max_x = new_min_x, new_max_x
    min_y, max_y = new_min_y, new_max_y
    min_z, max_z = new_min_z, new_max_z
    min_w, max_w = new_min_w, new_max_w


print(f"Cubes after six cycles: {len(state)}")