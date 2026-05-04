import pyray as rl
from typing_extensions import NamedTuple

from my_dataclasses import Player
from data.items import item_data
from data.weapons import weapon_data
from data.armor import armor_data
from data.bracelets import bracelet_data
from data.necklaces import necklace_data
from data.rings import ring_data
import utilities as u

from ui_info import scale

img_size = 8 * scale

three = 3 * scale
five = 5 * scale
six = 6 * scale
spacing = 1
spacing_height = spacing * 4

stats_size = rl.Vector2(64 * scale, 19 * scale)
equips_size = rl.Vector2(64 * scale, 42 * scale)
inventory_size = rl.Vector2(64 * scale, 64 * scale)
description_size = rl.Vector2(36 * scale, 64 * scale)

total_size = rl.Vector2(stats_size.x + three + inventory_size.x + three + description_size.x, inventory_size.y)
center = rl.Vector2(rl.get_screen_width()//2, rl.get_screen_height()//2)
width = rl.get_screen_width()
rl.get_screen_height()

stats_pos = rl.Vector2(center.x - total_size.x//2, center.y - total_size.y//2)
stats_start = rl.Vector2(stats_pos.x + five, stats_pos.y + five)
stats_end = rl.Vector2(stats_pos.x + stats_size.x - five, stats_pos.y + stats_size.y - five)

equips_pos = rl.Vector2(stats_pos.x, stats_pos.y + stats_size.y + three)
equip_margin = 11 * scale

weapon_pos = rl.Vector2(equips_pos.x + six, equips_pos.y + six)
head_pos = rl.Vector2(weapon_pos.x + equip_margin, weapon_pos.y)
chest_pos = rl.Vector2(head_pos.x + equip_margin, weapon_pos.y)
legs_pos = rl.Vector2(chest_pos.x + equip_margin, weapon_pos.y)
feet_pos = rl.Vector2(legs_pos.x + equip_margin, weapon_pos.y)
equips_end = feet_pos.x + equip_margin

necklace_pos = rl.Vector2(weapon_pos.x, weapon_pos.y + equip_margin)
bracelet_pos = rl.Vector2(necklace_pos.x + equip_margin, necklace_pos.y)
ring_pos = rl.Vector2(bracelet_pos.x + equip_margin * 2, necklace_pos.y)

inventory_pos = rl.Vector2(stats_pos.x + stats_size.x + three, stats_pos.y)
item_pos = rl.Vector2(inventory_pos.x + six, inventory_pos.y + six)
item_height = 9
item_margin = 11 * scale
tab_size = rl.Vector2(8 * scale, 8 * scale)
tab_pos = rl.Vector2(inventory_pos.x, inventory_pos.y - 11 * scale)
tab_margin = 9 * scale

description_pos = rl.Vector2(inventory_pos.x + inventory_size.x + three, inventory_pos.y)
text_margin = six
text_start = rl.Vector2(description_pos.x + text_margin, description_pos.y + text_margin)
text_end = rl.Vector2(description_pos.x + description_size.x - text_margin, description_pos.y + description_size.y - text_margin)
text_area = rl.Vector2(text_end.x - text_start.x, text_end.y - text_start.y)


def draw_text(font: rl.Font, text: str, font_size: float, pos: rl.Vector2):
    centered = u.center_text(font, text, font_size, spacing, rl.Vector2(pos.x, pos.y), description_size.x, 0)
    rl.draw_text_ex(font, text.upper(), centered, font_size, spacing, rl.BLACK)

def draw_stats(font: rl.Font, font_size: int, player: Player, gold_count: int, textures: dict):
    rl.draw_texture_ex(textures["stats"], (stats_pos.x, stats_pos.y), 0, scale, rl.WHITE)
    size = rl.measure_text_ex(font, "Test", font_size, spacing)
    font_height = size.y

    p = player
    health = f"Health: {p.health + p.bonus_health} / {p.max_health + p.bonus_health} (+ {p.bonus_health})"
    defense = f"Defense: {p.defense + p.bonus_defense} (+ {p.bonus_defense})"
    strength = f"Strength: {p.strength + p.bonus_strength} (+ {p.bonus_strength})"
    attack_speed = f"Attack Speed: {p.attack_speed + p.bonus_attack_speed} (+ {p.bonus_attack_speed})"
    speed = f"Speed: {p.speed + p.bonus_speed} (+ {p.bonus_speed})"
    gold = f"{gold_count} Gold"

    pos = rl.Vector2(stats_start.x, stats_start.y)

    # Draw Health
    rl.draw_text_ex(font, health, rl.Vector2(pos.x, pos.y), font_size, spacing, rl.BLACK)
    pos.y += font_height + spacing_height

    # Draw stats
    stats = [defense, strength, gold, attack_speed, speed]
    for i in range(len(stats)):
        if i == 3:
            pos.x = stats_start.x + (stats_end.x - stats_start.x)//2
            pos.y = stats_start.y + font_height + spacing_height

        rl.draw_text_ex(font, stats[i], rl.Vector2(pos.x, pos.y), font_size, spacing, rl.BLACK)
        pos.y += font_height + spacing_height

    # Draw Gold




def draw_equips(inventory: dict, desc_item: str, mouse: rl.Vector2, textures: dict, equips: dict) -> str:
    remove_name = ""
    rl.draw_texture_ex(textures["equips"], equips_pos, 0, scale, rl.WHITE)

    types = {"weapons": weapon_pos, "armor head": head_pos, "armor chest": chest_pos, "armor legs": legs_pos, "armor feet": feet_pos,
             "necklaces": necklace_pos, "bracelets": bracelet_pos, "rings": ring_pos}
    for key, value in types.items():
        items = [(item_name, item) for item_name, item in equips.items() if item.type == key]

        pos = rl.Vector2(value.x, value.y)
        for name, item in items:
            for i in range(item.count):
                if pos.x <= mouse.x <= pos.x + img_size and pos.y <= mouse.y <= pos.y + img_size:
                    desc_item = f"{name}"
                    rl.draw_texture_ex(textures["highlight"], rl.Vector2(pos.x - scale, pos.y - scale), 0, scale, rl.WHITE)
                    if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT):
                        remove_name = name

                rl.draw_texture_ex(textures["blank_equip"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
                rl.draw_texture_ex(textures[name], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)

                pos.x += item_margin
                if pos.x == equips_end:
                    pos.x = weapon_pos.x
                    pos.y += item_margin


    if remove_name != "":
        item_type = equips[remove_name].type
        u.add_to_inventory(inventory[item_type.split(" ")[0]], remove_name, item_type, 1)
        u.remove_from_inventory(inventory["equips"], remove_name, 1)

    return desc_item

def draw_items(font: rl.Font, font_size: float, player: Player, inventory: dict, desc_item: str, mouse: rl.Vector2, textures: dict, items: dict) -> tuple[str, bool]:
    journal = False
    remove_name = ""
    rl.draw_texture_ex(textures["inventory"], inventory_pos, 0, scale, rl.WHITE)


    pos = rl.Vector2(item_pos.x, item_pos.y)
    for key, value in items.items():
        if pos.x <= mouse.x <= pos.x + img_size and pos.y <= mouse.y <= pos.y + img_size:
            desc_item = f"{key}"
            rl.draw_texture_ex(textures["highlight"], rl.Vector2(pos.x - scale, pos.y - scale), 0, scale, rl.WHITE)
            if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT) and not value.type in ("items", "consumables", "special"):
                remove_name = key
            if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT) and key == "journal":
                journal = True



        text = str(value.count)
        size = rl.measure_text_ex(font, text, font_size, spacing)

        rl.draw_texture_ex(textures[f"{key}"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
        rl.draw_text_ex(font, text, rl.Vector2(pos.x, pos.y + img_size - size.y//2), font_size, spacing, rl.BLACK)

        pos.x += item_margin
        if pos.x > item_pos.x + inventory_size.x:
            pos.x = item_pos.x
            pos.y += item_margin

    if remove_name != "":
        add = True
        value = items[remove_name]
        data = u.get_data(remove_name, value.type)

        for stat, num in data.requirements.items():
            if player.__getattribute__(stat) < num:
                add = False



        types = {"armor head": 1, "armor chest": 1, "armor legs": 1, "armor feet": 1,
                 "weapons": 1, "necklaces": 1, "bracelets": 2, "rings": 7}

        count = [item.count for item in inventory["equips"].values() if item.type == value.type]
        if count:
            total = 0
            for num in count:
                total += num
            if total >= types[value.type]:
                add = False

        if add:
            u.add_to_inventory(inventory["equips"], remove_name, value.type, 1)
            u.remove_from_inventory(inventory[value.type.split(" ")[0]], remove_name, 1)

    return desc_item, journal

def wrap_lines(font: rl.Font, text: str, font_size: float, text_width: int) -> list[str]:
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

def draw_wrapped_text(font: rl.Font, lines: list[str], pos: rl.Vector2, font_size, spacing, centered: bool = False):
    line_size = rl.Vector2(0, 0)
    x = 0
    for line in lines:
        line_size = rl.measure_text_ex(font, line, font_size, spacing)
        x = 0
        if centered:
            x -= line_size.x//2

        rl.draw_text_ex(font, line, rl.Vector2(pos.x + x, pos.y),font_size, spacing, rl.BLACK)
        pos.y += line_size.y + line_size.y // 4

    return rl.Vector2(line_size.x, line_size.y), rl.Vector2(pos.x + x, pos.y)


def draw_description(font: rl.Font, font_size: float, text_font_size: float, textures: dict, item_name: str):
    color = rl.BLACK
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


        # Draw Item Name
        name_size = rl.measure_text_ex(font, item.name, font_size, spacing)
        name_pos = rl.Vector2(text_start.x + text_area.x//2, text_start.y)
        lines = wrap_lines(font, item.name, font_size, int(text_area.x))
        draw_wrapped_text(font, lines, rl.Vector2(name_pos.x, name_pos.y), font_size, spacing, True)

        # Draw Description
        text_pos = rl.Vector2(text_start.x + text_area.x//2, name_pos.y + name_size.y + name_size.y//4)
        lines = wrap_lines(font, item.description, text_font_size, int(text_area.x))
        line_size, line_pos = draw_wrapped_text(font, lines, rl.Vector2(text_pos.x, text_pos.y), text_font_size, spacing, True)
        y_margin = line_size.y + line_size.y // 4
        pos = rl.Vector2(text_start.x, line_pos.y + y_margin * 1.5)

        if not item.type in ("items", "special", "consumables"):
            # Draw Requirements
            for stat, num in item.requirements.items():
                rl.draw_text_ex(font, f"Requires: {num} {stat}", rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
                pos.y += y_margin
            # Draw Stats
            for stat, num in item.effects.items():
                rl.draw_text_ex(font, f"{stat} + {num}", rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
                pos.y += y_margin

        elif item.type in ("items", "special", "consumables"):
            # Draw Uses
            for use in item.uses:
                rl.draw_text_ex(font, f"Uses: {use}", rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
                pos.y += y_margin

        # Draw Locations
        for location in item.locations:
            rl.draw_text_ex(font, f"Locations: {location}", rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
            pos.y += y_margin


def draw_inv_tabs(mouse: rl.Vector2, textures: dict, types: list[str], inv_view: str) -> str:
    view = inv_view
    pos = rl.Vector2(tab_pos.x, tab_pos.y)
    for item_type in types:
        if inv_view == item_type:
            y = - 2 * scale
        else:
            y = 0
        rl.draw_texture_ex(textures[f"tab_{item_type}"], rl.Vector2(pos.x, pos.y + y), 0, scale, rl.WHITE)

        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            if pos.x + scale <= mouse.x <= pos.x + scale + tab_size.x and pos.y + scale<= mouse.y <= pos.y + scale + tab_size.y:
                view = item_type

        pos.x += tab_margin

    return view

def draw_inventory(font, font_size, player: Player, inventory:dict, gold: int, textures: dict, inv_view: str) -> tuple[str, bool]:
    text_font_size = font_size * .75
    tabs = {
        "weapons": ["weapons"],
        "armor": ["armor"],
        "accessories": ["necklaces", "bracelets", "rings"],
        "items": ["items"],
        "consumables": ["consumables"],
        "special": ["special"]
    }
    desc_item = ""
    mouse = rl.get_mouse_position()

    draw_stats(font, text_font_size, player, gold, textures)

    desc_item = draw_equips(inventory, desc_item, mouse, textures, inventory["equips"])

    inventories = {}
    for category in tabs[inv_view]:
        inventories.update(inventory[category])

    desc_item, journal = draw_items(font, font_size, player, inventory, desc_item, mouse, textures, inventories)

    inv_view = draw_inv_tabs(mouse, textures, list(tabs.keys()), inv_view)

    draw_description(font, font_size, text_font_size, textures, desc_item)

    return inv_view, journal
