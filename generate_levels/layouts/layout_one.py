import os
import pyray as rl
import random

from utilities import utilities as u
from utilities.get_data import get_npc
from classes.Tile import Tile
from classes.Npc import Npc

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

def create_npc(tile_pos: str) -> Npc:
    npc = get_npc(1)
    npc.pos = tile_pos
    return npc

def get_layout(door_pos: rl.Vector2, tile_size: int) -> dict:
    tiles = {}
    monsters = {}
    chests = {}
    npcs = {}
    size = 3
    start_pos = rl.Vector2(door_pos.x - (size//2) * tile_size, door_pos.y - (size * tile_size))
    for y in range(size):
        for x in range(size):
            tile_pos = rl.Vector2(start_pos.x + (x * tile_size), start_pos.y + (y * tile_size))
            tile_key = u.v2_str(tile_pos)
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


            tiles[tile_key] = [Tile (
                rotation = 0,
                name = name,
                directions = directions,
            )]


            tiles.update(get_wall(rl.Vector2(tile_pos.x, tile_pos.y), x, y, size, tile_size, door_pos))

            if y == 0 and x == 1:
                npc = create_npc(tile_key)
                npcs[tile_key] = npc




    return {"tiles": tiles, "monsters": monsters, "chests": chests, "npcs": npcs}
