import pyray as rl
import pickle
from my_dataclasses import GameState, Tile, Entity, InventoryItem
from data.monster import monster_data



def str_v2(string: str) -> rl.Vector2:
    # pos_x, pos_y = string.split(",")
    # x = pos_x.split(".")[0]
    # y = pos_y.split(".")[0]
    #
    # return rl.Vector2(int(x), int(y))
    x, y = string.split(",")
    return rl.Vector2(float(x), float(y))

def v2_str(v2: rl.Vector2) -> str:
    return f"{v2.x},{v2.y}"

def center_text(font: rl.Font, text: str, font_size: float, spacing: float, pos: rl.Vector2, width: float, height: float) -> rl.Vector2:
    text_pos = rl.Vector2(0, 0)
    size = rl.measure_text_ex(font, text, font_size, spacing)
    text_pos.x = (width//2) - (size.x//2) + pos.x
    text_pos.y = (height//2) - (size.y//2) + pos.y

    return text_pos


def add_to_inventory(state: GameState, item_name: str, inv_name: str, item_type: str, count: int):
    inventory = state.inventory[inv_name]

    if item_name in inventory.keys():
        inventory[item_name].count += count
    else:
        inventory[item_name] = InventoryItem(
            count = count,
            type = item_type,
        )

def remove_from_inventory(state: GameState, item_name: str, inv_name: str, count: int):
    inventory = state.inventory[inv_name.split(" ")[0]]
    if item_name in inventory.keys():
        if inventory[item_name].count == count:
            inventory.pop(item_name)
        else:
            inventory[item_name].count -= count



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
        player = (p.pos.x, p.pos.y, p.image, p.health, p.max_health, p.defense, p.strength, p.attack_speed, p.speed, p.last_attack)
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

        p = state.player
        p.pos.x, p.pos.y, p.image, p.health, p.max_health, p.defense, p.strength, p.attack_speed, p.speed, p.last_attack = data["player"]

        # (state.player.pos.x, state.player.pos.y, state.player.image, state.player.health, state.player.max_health) = data["player"]

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
        name = monster.name,
        image = name,
        health = monster.health,
        max_health = monster.health,
        defense = monster.defense,
        strength = monster.strength,
        attack_speed = monster.attack_speed,
        speed = monster.speed,
        last_attack = 0,
        stats = monster.stats,
        drops = monster.drops,
        locations = monster.locations,
    )


# def is_next_to(tile_size: int, v1: rl.Vector2, v2: rl.Vector2) -> bool:
#     x_diff = v1.x - v2.x
#     y_diff = v1.y - v2.y
#
#     if (x_diff == tile_size or x_diff == -tile_size) and y_diff == 0:
#         return True
#     if (y_diff == tile_size or y_diff == -tile_size) and x_diff == 0:
#         return True
#
#     return False
