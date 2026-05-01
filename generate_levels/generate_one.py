import os
import pyray as rl
import random

from my_dataclasses import GameState, Tile, Entity, Building
from generate_levels.layouts.layout_one import get_layout
import utilities as u

def opposite_direction(direction: str) -> str:
    if direction == "north":
        return "south"
    elif direction == "south":
        return "north"
    elif direction == "west":
        return "east"
    elif direction == "east":
        return "west"

    return ""

def get_direction_options(pos: rl.Vector2, start: rl.Vector2, end: rl.Vector2) -> list[str]:
    options = []
    if pos.x != start.x:
        options.append("west")
    if pos.x != end.x:
        options.append("east")
    if pos.y != start.y:
        options.append("north")
    if pos.y != end.y:
        options.append("south")
    return options

def create_tile(pos: rl.Vector2, name: str, tile_size: int, start: rl.Vector2, end: rl.Vector2, level: dict, building_tiles: list) -> Tile:
    directions = []

    # key_west = u.v2_str(u.pos_from_direction(tile_size, "west", rl.Vector2(pos.x, pos.y)))
    # key_north = u.v2_str(u.pos_from_direction(tile_size, "north", rl.Vector2(pos.x, pos.y)))
    # key_east = u.v2_str(u.pos_from_direction(tile_size, "east", rl.Vector2(pos.x, pos.y)))

    direction_options = get_direction_options(rl.Vector2(pos.x, pos.y), rl.Vector2(start.x, start.y), rl.Vector2(end.x, end.y))
    for direction in direction_options:
        opposite = opposite_direction(direction)
        key = u.v2_str(u.pos_from_direction(tile_size, direction, rl.Vector2(pos.x, pos.y)))

        if key in level.keys():
            if opposite in level[key].directions:
                directions.append(direction)
        elif not key in building_tiles:
            directions.append(direction)

        # if key_west in level.keys():
        #     directions.append("west")
        #
        # if key_north in level.keys():
        #     directions.append("north")
        #
        # if pos.x != end.x and not key_east in building_tiles:
        #     directions.append("east")
        # if pos.y != end.y:
        #     directions.append("south")

    images = [image.split(".")[0] for image in os.listdir("images/tiles") if image.split(".")[0].split("_")[0] == name]

    return Tile (
        rotation = 0,
        name = random.choice(images),
        directions = directions,
    )


def create_building(pos: rl.Vector2, tile_size: int, biome: str, level: dict) -> tuple[Tile, list[str], dict[str, dict]]:
    width = 3
    height = 3
    tiles = []
    door = ""

    building_types = ["tent",] #"shop", "house"]
    building_type = random.choice(building_types)
    name = f"{biome}_{building_type}"
    count = len(os.listdir(f"images/building/one/{biome}/{building_type}"))
    building_num = random.randint(1, count)

    # layout = layout_data[random.choice(list(layout_data.keys()))]



    for y in range(height):
        for x in range(width):
            pos2 = rl.Vector2(x * tile_size + pos.x, y * tile_size + pos.y)
            key = u.v2_str(rl.Vector2(pos2.x, pos2.y))
            if y + 1 == 3 and x + 1 == 2:
                door = key
            tiles.append(key)

            key_north = u.v2_str(u.pos_from_direction(tile_size, "north", rl.Vector2(pos2.x, pos2.y)))
            key_west = u.v2_str(u.pos_from_direction(tile_size, "west", rl.Vector2(pos2.x, pos2.y)))

            if key_north in level.keys():
                north = level[key_north]
                if "south" in north.directions:
                    north.directions.remove("south")

            if key_west in level.keys():
                west = level[key_west]
                if "east" in west.directions:
                    west.directions.remove("east")

    layout = get_layout(u.str_v2(door), tile_size, "plains", "house")

    building =  Tile (
        rotation = 0,
        name = f"{name}_{building_num}",
        directions = [],
    )

    return building, tiles, {door: layout}

def create_level(tile_size: int, map_size: int) -> tuple[rl.Vector2, dict, dict, dict, dict]:
    """
    :param tile_size:
    :param map_size:
    :return: start position, tiles/buildings in the level, monsters in the level, chests in the level, doors in the level
    """
    level = {}
    monsters = {}
    chests = {}
    center = map_size//2 * tile_size
    # start_pos = rl.Vector2(center, center)
    start_pos = rl.Vector2(144,240)
    doors = {}
    building_tiles = []
    end = (map_size * tile_size) - tile_size
    end_pos = rl.Vector2(end, end)

    biome = "plains"
    for y in range(map_size):
        for x in range(map_size):
            pos = rl.Vector2(x * tile_size, y * tile_size)
            key = u.v2_str(rl.Vector2(pos.x, pos.y))

            if x < 5 and y == 0:
                monsters[key] = u.create_entity("weak_grass_tuft")

            if y == 2 and x == 2:
                building, tiles, door = create_building(rl.Vector2(pos.x, pos.y), tile_size, biome, level)
                building_tiles.extend(tiles)
                level[key] = building
                doors.update(door)

            if not key in building_tiles:
                level[key] = create_tile(rl.Vector2(pos.x, pos.y), "grass", tile_size, rl.Vector2(0, 0), rl.Vector2(end_pos.x, end_pos.x), level, building_tiles)






    return start_pos, level, monsters, chests, doors
