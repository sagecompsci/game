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


def get_adjacent_tiles(view: dict, player_pos: rl.Vector2, tile_size) -> list:
    tiles = []
    key = v2_str(rl.Vector2(player_pos.x, player_pos.y))
    directions = view["tiles"][key][0].directions
    for direction in directions:
        pos = pos_from_direction(tile_size, direction, rl.Vector2(player_pos.x, player_pos.y))
        tiles.append(v2_str(rl.Vector2(pos.x, pos.y)))
    return tiles

def is_mouse_on_tile(camera: rl.Camera2D, tile_key: str, tile_size: float) -> bool:
    screen_mouse = rl.get_mouse_position()
    mouse = rl.get_screen_to_world_2d(screen_mouse, camera)
    pos = str_v2(tile_key)

    if pos.x < mouse.x < pos.x + tile_size and pos.y < mouse.y < pos.y + tile_size:
        return True

    return False


def wrap_lines(font: rl.Font, text: str, font_size: float, spacing: float, text_width: int) -> list[str]:
    lines_list = []
    lines = []
    text_size = rl.measure_text_ex(font, text, font_size, spacing)
    if text_size.x > text_width:
        words = text.split(" ")
        line = []
        while len(words) > 0:
            if not line:
                line.append(words[0])
                words.pop(0)
                while True:
                    if len(words) <= 0:
                        lines_list.append(line.copy())
                        break

                    line.append(words[0])
                    if rl.measure_text_ex(font, " ".join(line), font_size, spacing).x > text_width:
                        line.pop(-1)
                        lines_list.append(line.copy())
                        line = []
                        break

                    else:
                        words.pop(0)

    else:
        lines = [text]

    for line in lines_list:
        lines.append(" ".join(line))

    return lines

def draw_wrapped_text(font: rl.Font, lines: list[str], pos: rl.Vector2, font_size, spacing, color, centered: bool = False):
    pos = rl.Vector2(pos.x, pos.y)
    line_size = rl.Vector2(0, 0)
    x = 0
    for line in lines:
        line_size = rl.measure_text_ex(font, line, font_size, spacing)
        x = 0
        if centered:
            x -= line_size.x//2

        rl.draw_text_ex(font, line, rl.Vector2(pos.x + x, pos.y),font_size, spacing, color)
        pos.y += line_size.y + line_size.y // 4

    return rl.Vector2(line_size.x, line_size.y), rl.Vector2(pos.x + x, pos.y)

def give_quest(available_quests: dict, active_quests: dict, quest_code: int):
    if quest_code in available_quests.keys():
        active_quests[quest_code] = available_quests[quest_code]
        available_quests.pop(quest_code)
