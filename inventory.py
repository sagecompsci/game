import pyray as rl
from my_dataclasses import InventoryItem, GameState
from data.items import item_data
from data.weapons import weapon_data
from data.armor import armor_data
from data.bracelets import bracelet_data
from data.necklaces import necklace_data
from data.rings import ring_data
import utilities as u
import math

scale = rl.get_screen_width()//140
img_size = 8 * scale
height = 48 * scale
item_margin = 1 * scale
inventory_margin = 1 * scale

equips_width = 48 * scale
items_width = 48 * scale
description_width = 21 * scale

button_scale = scale//6
button_size = rl.Vector2(64 * button_scale, 16 * button_scale)
button_margin = 1 * scale

font = rl.get_font_default()
spacing = .5 * scale
font_size = 2 * scale

name_size = 4 * scale
count_margin = 1 * scale
text_margin = 1 * scale
border = 2 * scale

total_width = equips_width + items_width + description_width + (inventory_margin * 3)
start_x = (rl.get_screen_width()//2) - (total_width//2)
start_y = rl.get_screen_height()//2 - height//2
equips_pos = rl.Vector2(start_x, start_y )
items_pos = rl.Vector2(equips_pos.x + equips_width + inventory_margin, start_y)
description_pos = rl.Vector2(items_pos.x + items_width + inventory_margin, start_y)

button_pos = rl.Vector2(items_pos.x, items_pos.y - button_size.y - button_margin)

stat_pos = rl.Vector2(
    border + equips_pos.x,
    border + equips_pos.y)
stat_pos_end = rl.Vector2(
    equips_pos.x + equips_width - border,
    18 * scale + equips_pos.y
)

weapon_pos = rl.Vector2(
    border + equips_pos.x,
    20 * scale + equips_pos.y)
head_pos = rl.Vector2(weapon_pos.x + img_size + item_margin, weapon_pos.y)
chest_pos = rl.Vector2(head_pos.x + img_size + item_margin, weapon_pos.y)
leg_pos = rl.Vector2(chest_pos.x + img_size + item_margin, weapon_pos.y)
feet_pos = rl.Vector2(leg_pos.x + img_size + item_margin, weapon_pos.y)

necklace_pos = rl.Vector2(weapon_pos.x, weapon_pos.y + img_size + item_margin)
bracelet_pos = rl.Vector2(necklace_pos.x + img_size + item_margin, necklace_pos.y)
ring_pos = rl.Vector2(bracelet_pos.x + (img_size + item_margin) * 2, necklace_pos.y)
equip_end = equips_pos.x + border + (img_size + item_margin) * 5

item_pos_start = rl.Vector2(
    border + items_pos.x,
    border + items_pos.y)

description_text_start = rl.Vector2(
    border + description_pos.x,
    22 * scale + description_pos.y)

description_image_start = rl.Vector2(
    3 * scale + description_pos.x,
    3 * scale + description_pos.y)

def draw_text(text: str, font_size: float, pos: rl.Vector2):
    centered = u.center_text(font, text, font_size, spacing, rl.Vector2(pos.x, pos.y), description_width, 0)
    rl.draw_text_ex(font, text, centered, font_size, spacing, rl.BLACK)

def draw_stats(state: GameState):
    size = rl.measure_text_ex(font, "Test", font_size, spacing)
    font_height = size.y

    p = state.player
    health = f"Health: {math.trunc(p.health)} / {math.trunc(p.max_health)} (+{math.trunc(p.bonus_health)})"
    defense = f"Defense: {math.trunc(p.defense)} (+{math.trunc(p.bonus_defense)})"
    strength = f"Strength: {math.trunc(p.strength)} (+{math.trunc(p.bonus_strength)})"
    attack_speed = f"Attack Speed: {math.trunc(p.attack_speed)} (+{math.trunc(p.bonus_attack_speed)})"
    speed = f"Speed: {math.trunc(p.speed)} (+{math.trunc(p.bonus_speed)})"
    gold = f"{state.gold} Gold"

    stats = [health, defense, strength, attack_speed, speed, gold]
    pos = rl.Vector2(stat_pos.x, stat_pos.y)
    for i in range(len(stats)):
        x = pos.x
        rl.draw_text_ex(font, stats[i], rl.Vector2(x, pos.y), font_size, spacing, rl.BLACK)
        pos.y += font_height + border//2


def draw_equips(state: GameState, desc_item: str, mouse: rl.Vector2, textures: dict, equips: dict) -> str:
    remove_name = ""
    rl.draw_texture_ex(textures["equips"], equips_pos, 0, scale, rl.WHITE)
    draw_stats(state)

    types = {"weapons": weapon_pos, "armor head": head_pos, "armor chest": chest_pos, "armor legs": leg_pos, "armor feet": feet_pos,
             "necklaces": necklace_pos, "bracelets": bracelet_pos, "rings": ring_pos}
    for key, value in types.items():
        items = [(item_name, item) for item_name, item in equips.items() if item.type == key]

        pos = rl.Vector2(value.x, value.y)
        for name, item in items:
            for i in range(item.count):
                if pos.x <= mouse.x <= pos.x + img_size and pos.y <= mouse.y <= pos.y + img_size:
                    desc_item = f"{name}"
                    if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT):
                        remove_name = name

                rl.draw_texture_ex(textures["blank"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
                rl.draw_texture_ex(textures[name], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)

                pos.x += img_size + item_margin
                if pos.x == equip_end:
                    pos.x = weapon_pos.x
                    pos.y += img_size + item_margin


    if remove_name != "":
        item_type = equips[remove_name].type
        u.add_to_inventory(state, remove_name, item_type.split(" ")[0], item_type, 1)
        u.remove_from_inventory(state, remove_name, "equips", 1)
        # state.inventory["equips"].pop(remove_name)

    return desc_item

def draw_items(state: GameState, desc_item: str, mouse: rl.Vector2, textures: dict, items: dict) -> str:
    remove_name = ""
    rl.draw_texture_ex(textures["items"], items_pos, 0, scale, rl.WHITE)

    pos = rl.Vector2(item_pos_start.x, item_pos_start.y)
    for key, value in items.items():
        if pos.x <= mouse.x <= pos.x + img_size and pos.y <= mouse.y <= pos.y + img_size:
            desc_item = f"{key}"
            if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT) and value.type != "item":
                remove_name = key


        text = str(value.count)
        size = rl.measure_text_ex(font, text, font_size, spacing)
        count_pos = rl.Vector2(
            pos.x + img_size - size.x - count_margin,
            pos.y + img_size - size.y - count_margin,
        )

        rl.draw_texture_ex(textures[f"{key}"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
        rl.draw_text_ex(font, text, rl.Vector2(count_pos.x, count_pos.y), font_size, spacing, rl.WHITE)

        pos.x += img_size + item_margin
        if pos.x > items_pos.x + items_width:
            pos.x = item_pos_start.x
            pos.y += img_size + item_margin

    if remove_name != "":
        value = items[remove_name]

        types = {"armor head": 1, "armor chest": 1, "armor legs": 1, "armor feet": 1,
                 "weapons": 1, "necklaces": 1, "bracelets": 2, "rings": 7}
        equips = [item for item in state.inventory["equips"].values()]

        count = [item.count for item in state.inventory["equips"].values() if item.type == value.type]
        add = True
        if count:
            total = 0
            for num in count:
                total += num
            if total >= types[value.type]:
                add = False

        if add:
            u.add_to_inventory(state, remove_name, "equips", value.type, 1)
            u.remove_from_inventory(state, remove_name, value.type, 1)

    return desc_item

def draw_description(textures: dict, item_name: str):
    rl.draw_texture_ex(textures["description"], description_pos, 0, scale, rl.WHITE)

    if item_name != "":
        if item_name in item_data.keys():
            item = item_data[item_name]
        elif item_name in weapon_data.keys():
            item = weapon_data[item_name]
        elif item_name in armor_data.keys():
            item = armor_data[item_name]
        elif item_name in necklace_data.keys():
            item = necklace_data[item_name]
        elif item_name in bracelet_data.keys():
            item = bracelet_data[item_name]
        elif item_name in ring_data.keys():
            item = ring_data[item_name]

        rl.draw_texture_ex(textures[item_name], description_image_start, 0, 2 * scale, rl.WHITE)
        pos = rl.Vector2(description_text_start.x, description_text_start.y)

        draw_text(item_name, name_size, pos)

        name_height = rl.measure_text_ex(font, item_name, name_size, spacing)
        pos.y += name_height.y + text_margin


        content = [f"{item.description}"]
        if item_name in item_data:
            content.append(f"{item.uses}")
        else:
            content.extend([f"{item.effects}", f"{item.requirements}"])

        content.append(f"{item.locations}")

        text_size = rl.measure_text_ex(font, "Test", font_size, spacing)
        for string in content:
            draw_text(string, font_size, rl.Vector2(pos.x, pos.y))
            pos.y += text_size.y + text_margin


def draw_inv_buttons(mouse: rl.Vector2, textures: dict, types: list[str], inv_view: str) -> str:
    view = inv_view
    pos = rl.Vector2(button_pos.x, button_pos.y)
    for item_type in types:
        if inv_view == item_type:
            y = button_margin
        else:
            y = 0
        rl.draw_texture_ex(textures["blank_button"], rl.Vector2(pos.x, pos.y + y), 0, button_scale, rl.WHITE)
        text_pos = u.center_text(font, item_type, font_size, spacing, rl.Vector2(pos.x, pos.y + y), button_size.x, button_size.y)
        rl.draw_text_ex(font, item_type, rl.Vector2(text_pos.x, text_pos.y), font_size, spacing, rl.WHITE)

        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            if pos.x <= mouse.x <= pos.x + button_size.x and pos.y <= mouse.y <= pos.y + button_size.y:
                view = item_type

        pos.x += button_margin + button_size.x

    return view

def draw_inventory(state: GameState, textures: dict, inventory: dict, gold: int):
    desc_item = ""
    mouse = rl.get_mouse_position()

    desc_item = draw_equips(state, desc_item, mouse, textures, inventory["equips"])
    desc_item = draw_items(state, desc_item, mouse, textures, inventory[state.inv_view])

    state.inv_view = draw_inv_buttons(mouse, textures, ["weapons", "armor", "necklaces", "bracelets", "rings", "items"], state.inv_view)

    draw_description(textures, desc_item)
