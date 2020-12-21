from functools import reduce

with open("input/input20.txt") as f:
    content = f.read().splitlines()


def string_to_list(the_string):
    the_list = []
    the_list[:0] = the_string
    return the_list


class Tile:

    def __init__(self, tile_id):
        self.tile_id = tile_id
        self.image_data = []
        self.borders = []
        self.possible_adjacent_tiles = []

    def init_borders(self):
        self.borders.append(self.image_data[0])
        self.borders.append(self.image_data[-1])
        transposed = list(map(list, zip(*self.image_data)))
        self.borders.append(transposed[0])
        self.borders.append(transposed[-1])

    def has_matching_border(self, other_tile):
        for border in self.borders:
            for other_border in other_tile.borders:
                if border == other_border or border == list(reversed(other_border)):
                    return True
        return False


tiles = {}
curr_tile_id = None
for line in content:
    if not line:
        tiles[curr_tile_id].init_borders()
        curr_tile_id = None
    elif line.startswith("Tile"):
        curr_tile_id = int(line[5:-1])
        tiles[curr_tile_id] = Tile(curr_tile_id)
    else:
        tiles[curr_tile_id].image_data.append(string_to_list(line))

tile_ids = list(tiles.keys())
for i in range(0, len(tile_ids)):
    tile = tiles[tile_ids[i]]
    for j in range(i + 1, len(tile_ids)):
        curr_tile = tiles[tile_ids[j]]
        if tile.has_matching_border(curr_tile):
            tile.possible_adjacent_tiles.append(curr_tile.tile_id)
            curr_tile.possible_adjacent_tiles.append(tile.tile_id)

corner_ids = []
for tile_id, tile in tiles.items():
    if len(tile.possible_adjacent_tiles) == 2:
        corner_ids.append(tile_id)

print("Solution 1: the product of the IDs of the corner tiles is {}".format(reduce(lambda x, y: x * y, corner_ids)))
print("Solution 2: {}".format(0))
