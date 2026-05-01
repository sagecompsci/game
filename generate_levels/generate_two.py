import pyray as rl
import random
from data.weapons import weapon_data

import utilities as u
from my_dataclasses import GameState, Tile



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

        pos2_str = u.v2_str(rl.Vector2(pos2.x, pos2.y))
        if pos2_str in maze.keys():
            opposite = get_opposite_direction(direction)
            if opposite in maze[pos2_str].directions:
                directions.append(direction)

        elif 0 <= pos2.x <= (state.map_size * state.tile_size) - state.tile_size and 0 <= pos2.y <= (state.map_size * state.tile_size) - state.tile_size:
            possible_directions.append(direction)

    return directions, possible_directions

def get_index(paths: list[dict], key: str) -> int:
    for i in range(len(paths)):
        if key in paths[i].keys():
            return i
    return 0


def get_current_path(state: GameState, paths: list[dict], pos: rl.Vector2, directions: list[str]) -> tuple[list[dict], int]:
    if len(directions) == 2:
        north = u.pos_from_direction(state.tile_size, "north", rl.Vector2(pos.x, pos.y))
        west = u.pos_from_direction(state.tile_size, "west", rl.Vector2(pos.x, pos.y))
        north_index = get_index(paths, u.v2_str(rl.Vector2(north.x, north.y)))
        west_index = get_index(paths, u.v2_str(rl.Vector2(west.x, west.y)))

        if north_index != west_index:
            paths[north_index].update(paths[west_index])
            paths.pop(west_index)
            north_index = get_index(paths, u.v2_str(rl.Vector2(north.x, north.y)))


        index = north_index

    elif len(directions) == 1:
        pos2 = u.pos_from_direction(state.tile_size, f"{directions[0]}", rl.Vector2(pos.x, pos.y))
        index = get_index(paths, u.v2_str(rl.Vector2(pos2.x, pos2.y)))

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

    current_key = u.v2_str(rl.Vector2(pos.x, pos.y))
    path = {current_key: list(directions)}
    if create_new_path:
        paths.append(path)
        paths, index = get_current_path(state, paths, rl.Vector2(pos.x, pos.y), directions)
        current_path = paths[index]
    else:
        current_path.update(path)

    if not create_new_path:
        for direction in directions:
            prev_key = u.v2_str(u.pos_from_direction(state.tile_size, direction, rl.Vector2(pos.x, pos.y)))
            opposite = get_opposite_direction(direction)
            if opposite in current_path[prev_key]:
                current_path[current_key].remove(direction)
                current_path[prev_key].remove(opposite)

                if len(current_path[prev_key]) == 0:
                    current_path.pop(prev_key)
    end = rl.Vector2((state.map_size - 1) * state.tile_size)
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
    return directions, paths

def create_tile(state: GameState, maze: dict, pos: rl.Vector2, paths: list[dict], dead_ends: list[rl.Vector2],
                directions: list[str] = None) -> tuple[Tile, list[dict], list[rl.Vector2]]:

    if directions is None:
        directions, paths = get_directions(state, maze, pos, paths)

    tile = get_tile(directions)
    if tile == "one":
        dead_ends.append(rl.Vector2(pos.x, pos.y))
    rotation = get_rotation(tile, directions)


    tile = Tile (
        rotation = rotation,
        name= tile,
        directions = directions,
    )
    return tile, paths, dead_ends

def generate_chests_monsters(state: GameState, dead_ends: list, maze: dict) -> tuple[dict, dict]:
    chests = {}
    monsters = {}

    # Chests and Minotaurs in front of chests
    for i in range(state.map_size // 2):
        pos = random.choice(dead_ends)
        dead_ends.remove(pos)

        item = random.choice(list(weapon_data.keys()))
        chests[u.v2_str(rl.Vector2(pos.x, pos.y))] = item

        key = u.v2_str(rl.Vector2(pos.x, pos.y))
        monster_pos = u.pos_from_direction(state.tile_size, maze[key].directions[0], rl.Vector2(pos.x, pos.y))
        new_key = u.v2_str(rl.Vector2(monster_pos.x, monster_pos.y))

        if new_key in state.monsters.keys():
            directions = maze[new_key].directions
            for direction in directions:
                monster_pos = u.pos_from_direction(state.tile_size, direction, rl.Vector2(monster_pos.x, monster_pos.y))
                new_key = u.v2_str(rl.Vector2(monster_pos.x, monster_pos.y))
                if new_key in state.monsters.keys():
                    break

        monster_name = "minotaur"
        monsters[new_key] = u.create_entity(monster_name)


    # Gargoyles
    count = state.map_size // 2
    while count > 0:
        key = random.choice(list(maze.keys()))
        if not key in monsters.keys() and not key in chests.keys():
            count -= 1
            monsters[key] = u.create_entity("gargoyle")





    return chests, monsters


def create_maze(state: GameState) -> tuple[dict, rl.Vector2, dict, dict]:
    maze = {}
    paths = []
    dead_ends = []
    for y in range(state.map_size):
        for x in range(state.map_size):
            tile, paths, dead_ends = create_tile(state, maze, rl.Vector2(x * state.tile_size, y * state.tile_size), paths, dead_ends)

            string = u.v2_str(tile.pos)
            maze[string] = tile

    start_pos = random.choice(dead_ends)
    dead_ends.remove(start_pos)
    maze[u.v2_str(rl.Vector2(start_pos.x, start_pos.y))].name = "stair"

    chests, monsters = generate_chests_monsters(state, dead_ends, maze)


    return maze, start_pos, chests, monsters
