import os
import pyray as rl
import random

import utilities as u
from my_dataclasses import Tile

def get_wall(tile_pos: rl.Vector2, x: int, y: int, size: int, tile_size: int, door_pos: rl.Vector2) -> dict:
    tiles = {}
    x_edge = 0
    y_edge = 0

    if x == 0 or x == size - 1:
        x_edge = -tile_size
        rotation = 270
        wall_pos = rl.Vector2(tile_pos.x - tile_size, tile_pos.y)

        if x == size - 1:
            x_edge = tile_size
            rotation = 90
            wall_pos = rl.Vector2(tile_pos.x + tile_size, tile_pos.y)


        tiles[u.v2_str(rl.Vector2(wall_pos.x, wall_pos.y))] = [Tile(
            rotation = rotation,
            name = "wood_wall",
            directions = [],
        )]

    if y == 0 or y == size - 1:
        y_edge = -tile_size
        rotation = 0
        wall_pos = rl.Vector2(tile_pos.x, tile_pos.y - tile_size)

        if y == size - 1:
            y_edge = tile_size
            rotation = 180
            wall_pos = rl.Vector2(tile_pos.x, tile_pos.y + tile_size)

        if wall_pos.x == door_pos.x and wall_pos.y == door_pos.y:
            name = "wood_door"
            directions = ["north"]
        else:
            name = "wood_wall"
            directions = []



        tiles[u.v2_str(rl.Vector2(wall_pos.x, wall_pos.y))] = [Tile(
            rotation = rotation,
            name = name,
            directions = directions,
        )]

    if x_edge != 0 and y_edge != 0:
        rotation = 0

        if x == size - 1:
            rotation = 90
            if y == size - 1:
                rotation = 180

        elif x == 0 and y == size - 1:
            rotation = 270

        corner = rl.Vector2(tile_pos.x + x_edge, tile_pos.y + y_edge)
        tiles[u.v2_str(rl.Vector2(corner.x, corner.y))] = [Tile(
            rotation = rotation,
            name = "wood_corner",
            directions = [],
        )]

    return tiles

def get_layout(door_pos: rl.Vector2, tile_size: int, biome: str, building_type: str) -> dict:
    tiles = {}
    monsters = {}
    chests = {}
    size = 9
    start_pos = rl.Vector2(door_pos.x - (size//2) * tile_size, door_pos.y - (size * tile_size))
    for y in range(size):
        for x in range(size):
            tile_pos = rl.Vector2(start_pos.x + (x * tile_size), start_pos.y + (y * tile_size))
            tile_name = [tile.split(".")[0] for tile in os.listdir("images/tiles") if "stone_floor" in tile]
            name = random.choice(tile_name)

            directions = []
            if x != 0:
                directions.append("west")
            if x != size - 1:
                directions.append("east")
            if y != 0:
                directions.append("north")
            if y != size - 1 or (tile_pos.x == door_pos.x and tile_pos.y == door_pos.y - tile_size):
                directions.append("south")


            tiles[u.v2_str(rl.Vector2(tile_pos.x, tile_pos.y))] = [Tile (
                rotation = 0,
                name = name,
                directions = directions,
            )]


            tiles.update(get_wall(rl.Vector2(tile_pos.x, tile_pos.y), x, y, size, tile_size, door_pos))

    return {"tiles": tiles, "monsters": monsters, "chests": chests}




layout_data = {
    "plains_tent_1": {
        "tiles": {
            "144.0,144.0": Tile(
                rotation = 0,
                name = "two",
                directions = ["north"],
            ),
            "144.0,96.0": Tile (
                rotation = 180,
                name = "two",
                directions = ["south", "north"],
            ),
            "144.0,48.0": Tile(
                rotation=180,
                name="one",
                directions=["south"],
            ),
        },
        "chests": {},
        "monsters": {
            "144.0,48.0": u.create_entity("grass_tuft_weak")
        }
    },

}