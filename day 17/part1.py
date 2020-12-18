def count_neighbors(state, cube):
    cube_x, cube_y, cube_z = cube

    count = 0
    for offset_x in range(-1, 2):
        for offset_y in range(-1, 2):
            for offset_z in range(-1, 2):
                # skip the cube itself
                if offset_x == 0 and offset_y == 0 and offset_z == 0:
                    continue

                x = offset_x + cube_x
                y = offset_y + cube_y
                z = offset_z + cube_z

                if (x, y, z) in state:
                    count += 1

    return count


def print_state(state, min_x, max_x, min_y, max_y, min_z, max_z):
    for z in range(min_z, max_z + 1):
        print(f"z = {z}")
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y, z) in state:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print()


state = set()

min_x, max_x = 0, 0
min_y, max_y = 0, 0
min_z, max_z = 0, 0

for y, row in enumerate(open("day 17/input.txt").readlines()):
    for x, cube in enumerate(row):
        if cube == "#":
            state.add((x, y, 0))
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

print(state)
print(count_neighbors(state, (2, 2, 0)))
print(min_x, max_x)
print(min_y, max_y)
print(min_z, max_z)

print()
print()
print()

for _ in range(6):
    # print_state(state, min_x, max_x, min_y, max_y, min_z, max_z)
    # input()

    new_state = set()
    new_min_x, new_max_x = 0, 0
    new_min_y, new_max_y = 0, 0
    new_min_z, new_max_z = 0, 0

    for active_cube in state:
        for x in range(min_x - 1, max_x + 2):
            for y in range(min_y - 1, max_y + 2):
                for z in range(min_z - 1, max_z + 2):
                    cube = (x, y, z)
                    neighbor_count = count_neighbors(state, cube)

                    make_active = False
                    if cube in state:
                        if neighbor_count in [2, 3]:
                            make_active = True
                    else:
                        if neighbor_count == 3:
                            make_active = True

                    if make_active:
                        new_state.add(cube)
                        new_min_x, new_max_x = min(new_min_x, x), max(new_max_x, x)
                        new_min_y, new_max_y = min(new_min_y, y), max(new_max_y, y)
                        new_min_z, new_max_z = min(new_min_z, z), max(new_max_z, z)

    state = new_state
    min_x, max_x = new_min_x, new_max_x
    min_y, max_y = new_min_y, new_max_y
    min_z, max_z = new_min_z, new_max_z


print(f"Cubes after six cycles: {len(state)}")