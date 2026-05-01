import pyray as rl
import random

import utilities

size = 8
scale = 10
size *= scale

def get_checkerboard(tile1: str, tile2: str, pos: rl.Vector2) -> list[tuple[rl.Vector2, str]]:
    tiles = []
    for y in range(5):
        for x in range(5):
            texture = tile1
            if (x + y) % 2 == 0:
                texture = tile2
            new_pos = rl.Vector2(pos.x + (size * x), pos.y + (size * y))
            tiles.append((new_pos, texture))
    return tiles

def get_random(names: list[str], pos: rl.Vector2) -> list[tuple[rl.Vector2, str]]:
    tiles = []
    prev_choice = ""
    texture = ""
    for y in range(5):
        for x in range(5):
            while prev_choice == texture:
                texture = random.choice(names)

            prev_choice = texture
            new_pos = rl.Vector2(pos.x + (size * x), pos.y + (size * y))
            tiles.append((new_pos, texture))
    return tiles

def draw(tiles: list[tuple[rl.Vector2, str]], textures: dict[str, rl.Texture]):
    for tile in tiles:
        rl.draw_texture_ex(textures[tile[1]], rl.Vector2(tile[0].x, tile[0].y), 0, scale, rl.WHITE)


rl.init_window(1800, 900, "test")
textures = utilities.get_files("images")
tiles = get_random(["stone_floor_1", "stone_floor_2", "stone_floor_3"], rl.Vector2(0, 0))
# tiles = get_random(["grass_1", "grass_2", "grass_3"], rl.Vector2(0, 0))

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.LIGHTGRAY)

    draw(tiles, textures)

    rl.end_drawing()

