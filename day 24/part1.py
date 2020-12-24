from dataclasses import dataclass


@dataclass
class InvalidDirection(Exception):
    dir: str


@dataclass
class CubeCoordinates:
    x: int
    y: int
    z: int

    def from_direction(dir):
        if dir == "e":
            return CubeCoordinates(1, -1, 0)
        if dir == "se":
            return CubeCoordinates(0, -1, 1)
        if dir == "sw":
            return CubeCoordinates(-1, 0, 1)
        if dir == "w":
            return CubeCoordinates(-1, 1, 0)
        if dir == "nw":
            return CubeCoordinates(0, 1, -1)
        if dir == "ne":
            return CubeCoordinates(1, 0, -1)
        raise InvalidDirection(dir)

    def __add__(self, other):
        result = CubeCoordinates(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )
        # sanity
        assert result.x + result.y + result.z == 0
        return result

    def __str__(self):
        return f"({self.x} {self.y} {self.x})"

    def __hash__(self):
        return hash(str(self))


# load the paths

paths = []

for path in open("day 24/input.txt").readlines():
    path_iter = iter(path.rstrip())
    tiles_to_flip = []
    while True:
        dir = next(path_iter, None)
        if dir in ["e", "w"]:
            tiles_to_flip.append(dir)
        elif dir in ["s", "n"]:
            subdir = next(path_iter)
            if subdir not in ["e", "w"]:
                raise InvalidDirection(dir)
            tiles_to_flip.append(dir + subdir)
        elif dir is None:
            break
        else:
            raise InvalidDirection(dir)
    paths.append(tiles_to_flip)

for path in paths:
    print(path)


# flip the tiles at end of each path

black_tiles = set()

for path in paths:
    current_tile = CubeCoordinates(0, 0, 0)

    for move in path:
        current_tile += CubeCoordinates.from_direction(move)

    if current_tile not in black_tiles:
        print(f"Flip {current_tile} to black")
        black_tiles.add(current_tile)
    else:
        print(f"Flip {current_tile} to white")
        black_tiles.remove(current_tile)

print(f"Number of black tiles: {len(black_tiles)}")