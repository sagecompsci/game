import pyray as rl
import pickle
from my_dataclasses import GameState, Tile, Entity, Button
from monsters import monster_data



def str_v2(string: str) -> rl.Vector2:
    pos_x, pos_y = string.split(",")
    x = pos_x.split(".")[0]
    y = pos_y.split(".")[0]

    return rl.Vector2(int(x), int(y))

def v2_str(v2: rl.Vector2) -> str:
    return f"{v2.x},{v2.y}"

def is_next_to(tile_size: int, v1: rl.Vector2, v2: rl.Vector2) -> bool:
    x_diff = v1.x - v2.x
    y_diff = v1.y - v2.y

    if (x_diff == tile_size or x_diff == -tile_size) and y_diff == 0:
        return True
    if (y_diff == tile_size or y_diff == -tile_size) and x_diff == 0:
        return True

    return False

def pos_from_direction(tile_size: int, direction: str, pos: rl.Vector2) -> rl.Vector2:
    pos2 = rl.Vector2(pos.x, pos.y)
    if direction == "north":
        pos2.y -= tile_size
    elif direction == "south":
        pos2.y += tile_size
    elif direction == "east":
        pos2.x += tile_size
    elif direction == "west":
        pos2.x -= tile_size

    return pos2

def print_v2(pos: rl.Vector2):
    print(f"{pos.x}, {pos.y}")

def save(state: GameState):
    with open(f"saves/{state.save}.pickle", "wb") as f:
        maze = {}
        for key, value in state.maze.items():
            maze[key] = (value.pos.x, value.pos.y, value.rotate_pos.x, value.rotate_pos.y, value.rotation, value.tile, value.directions)

        p = state.player
        player = (p.pos.x, p.pos.y, p.image, p.level, p.xp, p.health, p.max_health)
        save_data = {
            "save": state.save,
            "player": player,
            "inventory": state.inventory,
            "gold": state.gold,
            "maze": maze,
            "monsters": state.monsters,
            "chests": state.chests,
            "time": state.time,
        }
        pickle.dump([save_data], f, 2)

    print("saved")

def read_file(name: str):
    with open(f"saves/{name}.pickle", "rb") as f:
        return pickle.load(f)

def load(name: str, state: GameState):
        data = read_file(name)[0]
        state.save = data["save"]

        (state.player.pos.x, state.player.pos.y, state.player.image, state.player.level, state.player.xp,
         state.player.health, state.player.max_health) = data["player"]

        state.inventory = data["inventory"]
        state.gold = data["gold"]


        maze = data["maze"]
        for key, value in maze.items():
           state.maze[key] = Tile (
               pos = rl.Vector2(value[0], value[1]),
               rotate_pos = rl.Vector2(value[2], value[3]),
               rotation = value[4],
               tile = value[5],
               directions = value[6],
           )

        state.monsters = data["monsters"]
        state.chests = data["chests"]
        state.time = data["time"]

        state.camera.target = rl.Vector2(state.player.pos.x, state.player.pos.y)

def create_entity(name: str) -> Entity:
    monster = monster_data[name]
    return Entity(
        name=monster.name,
        image=name,
        health=monster.health,
        max_health=monster.max_health,
        defense=monster.defense,
        attack=monster.attack,
        speed=monster.speed,
        drops=monster.drops,
        locations=monster.locations
    )