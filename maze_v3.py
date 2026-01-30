from heapq import merge

import pyray as rl
from dataclasses import dataclass
import random


@dataclass
class Tile:
    pos: rl.Vector2
    rotate_pos: rl.Vector2
    rotation: int
    texture: rl.Texture
    tile: str
    directions: list[str]

@dataclass
class GameState:
    tile_size: int
    maze_size: int
    textures: dict
    camera: rl.Camera2D

def init():
    rl.init_window(1800, 900, "Maze")
    state = GameState(
        tile_size= 24,
        maze_size= 100,
        textures = {},
        camera = rl.Camera2D (),
    )

    state.camera.offset = rl.Vector2(0, 0)
    state.camera.target = rl.Vector2(0, 0)
    state.camera.rotation = 0
    state.camera.zoom = 1

    textures = [
        "one",
        "two",
        "two_c",
        "three",
        "four",
        "none",
    ]

    for texture in textures:
        state.textures[texture] = rl.load_texture(f"images/{texture}.png")

    return state

def str_v2(string: str) -> rl.Vector2:
    x, y = string.split(",")
    return rl.Vector2(int(x), int(y))

def v2_str(v2: rl.Vector2) -> str:
    return f"{v2.x},{v2.y}"

def pos_from_direction(state: GameState, direction: str, pos: rl.Vector2) -> rl.Vector2:
    pos2 = rl.Vector2(pos.x, pos.y)
    if direction == "north":
        pos2.y -= state.tile_size
    elif direction == "south":
        pos2.y += state.tile_size
    elif direction == "east":
        pos2.x += state.tile_size
    elif direction == "west":
        pos2.x -= state.tile_size

    return pos2

def rotate(state: GameState, pos: rl.Vector2, rotation: int) -> rl.Vector2:
    if rotation == 90:
        pos.x += state.tile_size
    elif rotation == 180:
        pos.y += state.tile_size
        pos.x += state.tile_size
    elif rotation == 270:
        pos.y += state.tile_size

    return pos

def get_opposite_direction(direction: str) -> str:
    opposite = ""
    if direction == "north":
        opposite = "south"
    elif direction == "south":
        opposite = "north"
    elif direction == "west":
        opposite = "east"
    elif direction == "east":
        opposite = "west"
    return opposite

def get_tile(directions: list[str]) -> str:
    tile = "none"
    if len(directions) == 1:
        tile = "one"
    elif len(directions) == 2:
        if directions[0] == get_opposite_direction(directions[1]):
            tile = "two"
        else:
            tile = "two_c"

    elif len(directions) == 3:
        tile = "three"
    elif len(directions) == 4:
        tile = "four"

    return tile

def get_rotation(tile: str, directions: list[str]) -> int:
    rotation = 0
    if tile == "one":
        if "east" in directions:
            rotation = 90
        elif "south" in directions:
            rotation = 180
        elif "west" in directions:
            rotation = 270

    elif tile == "two":
        if "east" in directions:
            rotation = 90

    elif tile == "two_c":
        if "south" in directions:
            rotation = 90
            if "west" in directions:
                rotation += 90
        elif "north" in directions and "west" in directions:
            rotation = 270

    elif tile == "three":
        if not "west" in directions:
            rotation = 90
        elif not "north" in directions:
            rotation = 180
        elif not "east" in directions:
            rotation = 270

    return rotation

def check_directions(state: GameState, maze: dict, pos: rl.Vector2) -> tuple[list, list]:
    directions = []
    possible_directions = []
    for i in range(4):
        pos2 = rl.Vector2(pos.x, pos.y)
        direction = ""
        if i == 0:
            pos2.x += state.tile_size
            direction = "east"
        elif i == 1:
            pos2.x -= state.tile_size
            direction = "west"
        elif i == 2:
            pos2.y += state.tile_size
            direction = "south"
        elif i == 3:
            pos2.y -= state.tile_size
            direction = "north"

        pos2_str = v2_str(rl.Vector2(pos2.x, pos2.y))
        if pos2_str in maze.keys():
            opposite = get_opposite_direction(direction)
            if opposite in maze[pos2_str].directions:
                directions.append(direction)

        elif 0 <= pos2.x <= (state.maze_size*state.tile_size) - state.tile_size and 0 <= pos2.y <= (state.maze_size*state.tile_size) - state.tile_size:
            possible_directions.append(direction)

    return directions, possible_directions

def get_index(paths: list[dict], key: str) -> int:
    for i in range(len(paths)):
        if key in paths[i].keys():
            return i
    return 0


def get_current_path(state: GameState, paths: list[dict], pos: rl.Vector2, directions: list[str]) -> tuple[list[dict], int]:
    if len(directions) == 2:
        north = pos_from_direction(state, "north", rl.Vector2(pos.x, pos.y))
        west = pos_from_direction(state, "west", rl.Vector2(pos.x, pos.y))
        north_index = get_index(paths, v2_str(rl.Vector2(north.x, north.y)))
        west_index = get_index(paths, v2_str(rl.Vector2(west.x, west.y)))

        if north_index != west_index:
            paths[north_index].update(paths[west_index])
            paths.pop(west_index)
            north_index = get_index(paths, v2_str(rl.Vector2(north.x, north.y)))


        index = north_index

    elif len(directions) == 1:
        pos2 = pos_from_direction(state, f"{directions[0]}", rl.Vector2(pos.x, pos.y))
        index = get_index(paths, v2_str(rl.Vector2(pos2.x, pos2.y)))

    else:
        index = -1

    return paths, index


def get_directions(state: GameState, maze: dict, pos: rl.Vector2, paths: list[dict]) -> tuple[list[str], list[dict]]:
    directions, possible_directions = check_directions(state, maze, rl.Vector2(pos.x, pos.y))
    create_new_path = False
    current_path = {}

    if paths:
        paths, index = get_current_path(state, paths, rl.Vector2(pos.x, pos.y), directions)
        if index == -1:
            create_new_path = True
        else:
            current_path = paths[index]
    else:
        create_new_path = True

    current_key = v2_str(rl.Vector2(pos.x, pos.y))
    path = {current_key: list(directions)}
    if create_new_path:
        paths.append(path)
        paths, index = get_current_path(state, paths, rl.Vector2(pos.x, pos.y), directions)
        current_path = paths[index]
    else:
        current_path.update(path)

    if not create_new_path:
        for direction in directions:
            prev_key = v2_str(pos_from_direction(state, direction, rl.Vector2(pos.x, pos.y)))
            opposite = get_opposite_direction(direction)
            if opposite in current_path[prev_key]:
                current_path[current_key].remove(direction)
                current_path[prev_key].remove(opposite)

                if len(current_path[prev_key]) == 0:
                    current_path.pop(prev_key)
    end = rl.Vector2((state.maze_size - 1) * state.tile_size)
    if (len(directions) == 0 or (len(current_path) == 1 and len(current_path[current_key]) == 0)) and (pos.x != end and pos.y != end):
        minimum = 1
    else:
        minimum = 0

    length = len(possible_directions)
    if length != 0:
        num = random.randint(minimum, length)
        for i in range(num):
            direction = random.choice(possible_directions)
            possible_directions.remove(direction)
            directions.append(direction)
            current_path[current_key].append(direction)

        if len(current_path[current_key]) == 0:
            current_path.pop(current_key)

    # print()
    # print()
    # print("PATH")
    # print(current_key)
    # print("current path")
    # for prev_key, value in current_path.items():
    #     print()
    #     print(f"{prev_key}", end=" ")
    #     for direction in value:
    #         print(direction, end=" ")
    # print()
    # print("all paths")
    # for path in paths:
    #     print()
    #     print("new path")
    #     for key, value in path.items():
    #         print(f"{key}", end=" ")
    #         for direction in value:
    #             print(direction, end=" ")
    #
    return directions, paths

def create_tile(state: GameState, maze: dict, pos: rl.Vector2, paths: list[dict], directions: list[str] = None) -> tuple[Tile, list[dict]]:
    if directions is None:
        directions, paths = get_directions(state, maze, pos, paths)

    tile = get_tile(directions)
    rotation = get_rotation(tile, directions)
    rotate_pos = rotate(state, rl.Vector2(pos.x, pos.y), rotation)
    texture = state.textures[tile]


    tile = Tile (
        pos = pos,
        rotate_pos = rotate_pos,
        rotation = rotation,
        texture = texture,
        tile = tile,
        directions = directions,
    )
    return tile, paths

def create_maze(state: GameState) -> dict:
    maze = {}
    paths = []
    for y in range(state.maze_size):
        for x in range(state.maze_size):
            tile, paths = create_tile(state, maze, rl.Vector2(x * state.tile_size, y * state.tile_size), paths)

            string = v2_str(tile.pos)
            maze[string] = tile


    return maze


def draw_maze(state: GameState, maze: dict):
    for tile in maze.values():
        rl.draw_texture_ex(tile.texture, tile.rotate_pos, tile.rotation, state.tile_size // 8, rl.WHITE)

def main():
    state = init()
    maze = create_maze(state)

    while not rl.window_should_close():
        speed = 5
        if rl.is_key_down(rl.KeyboardKey.KEY_W):
            state.camera.target.y -= speed
        if rl.is_key_down(rl.KeyboardKey.KEY_S):
            state.camera.target.y += speed
        if rl.is_key_down(rl.KeyboardKey.KEY_D):
            state.camera.target.x += speed
        if rl.is_key_down(rl.KeyboardKey.KEY_A):
            state.camera.target.x -= speed
        if rl.is_key_pressed(rl.KeyboardKey.KEY_Z):
            state.camera.zoom += 1
        if rl.is_key_pressed(rl.KeyboardKey.KEY_X):
            state.camera.zoom -= 1


        rl.begin_drawing()
        rl.clear_background(rl.WHITE)
        rl.begin_mode_2d(state.camera)
        draw_maze(state, maze)

        rl.end_mode_2d()
        rl.end_drawing()

main()
