import os
import pyray as rl
from my_dataclasses import Entity, InventoryItem

from data.armor import armor_data, Armor
from data.bracelets import bracelet_data, Bracelet
from data.items import item_data, Item
from data.monsters import monster_data, Monster
from data.necklaces import necklace_data, Necklace
from data.rings import ring_data, Ring
from data.weapons import weapon_data, Weapon


from collections import namedtuple

def get_data(item_name: str, item_type: str) -> Armor | Bracelet | Item | Monster | Necklace | Ring | Weapon:
    item_type = item_type.split(" ")[0]
    data = []
    if item_type == "armor":
        data = armor_data[item_name]
    elif item_type == "bracelets":
        data = bracelet_data[item_name]
    elif item_type == "items":
        data = item_data[item_name]
    elif item_type == "monsters":
        data = monster_data[item_name]
    elif item_type == "necklaces":
        data = necklace_data[item_name]
    elif item_type == "rings":
        data = ring_data[item_name]
    elif item_type == "weapons":
        data = weapon_data[item_name]

    return data

def get_files(path: str) -> dict:
    textures = {}
    files = os.listdir(path)
    for file in files:
        new_path = path + "/" + file
        if os.path.isfile(new_path):
            name = file.split(".")[0]
            textures[name] = rl.load_texture(new_path)
        elif os.path.isdir(new_path):
            textures.update(get_files(new_path))

    return textures


def str_v2(string: str) -> rl.Vector2:
    x, y = string.split(",")
    return rl.Vector2(float(x), float(y))

def v2_str(v2: rl.Vector2) -> str:
    return f"{v2.x},{v2.y}"

def print_v2(pos: rl.Vector2):
    print(f"{pos.x}, {pos.y}")



def rotate(tile_size: int, pos: rl.Vector2, rotation: int) -> rl.Vector2:
    if rotation == 90:
        pos.x += tile_size
    elif rotation == 180:
        pos.y += tile_size
        pos.x += tile_size
    elif rotation == 270:
        pos.y += tile_size

    return pos

def center_text(font: rl.Font, text: str, font_size: float, spacing: float, pos: rl.Vector2, width: float, height: float) -> rl.Vector2:
    text_pos = rl.Vector2(0, 0)
    size = rl.measure_text_ex(font, text, font_size, spacing)
    text_pos.x = (width//2) - (size.x//2) + pos.x
    text_pos.y = (height//2) - (size.y//2) + pos.y

    return text_pos

def x_center_screen(width: int) -> int:
    center = rl.get_screen_width()//2
    return center - (width//2)

def y_center_screen(height: int) -> int:
    center = rl.get_screen_height()//2
    return center - (height//2)



def add_to_inventory(inventory: dict, item_name: str, item_type: str, count: int):
    if item_name in inventory.keys():
        inventory[item_name].count += count
    else:
        inventory[item_name] = InventoryItem(
            count = count,
            type = item_type,
        )

def remove_from_inventory(inventory: dict, item_name: str, count: int):
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


