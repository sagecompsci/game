import pyray as rl

from classes.Player import Player
from information.ui import scale
from information import types, views
from utilities import utilities as u
from utilities.get_data import get_item
from utilities.inventory_util import edit_inventory

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
inventory_margin = six
item_pos = rl.Vector2(inventory_pos.x + inventory_margin, inventory_pos.y + inventory_margin)
item_height = 9
item_margin = 11 * scale
tab_size = rl.Vector2(8 * scale, 8 * scale)
tab_pos = rl.Vector2(inventory_pos.x, inventory_pos.y - 11 * scale)
tab_margin = 9 * scale

description_pos = rl.Vector2(inventory_pos.x + inventory_size.x + three, inventory_pos.y)
text_margin = rl.Vector2(three, six)
text_start = rl.Vector2(description_pos.x + text_margin.x, description_pos.y + text_margin.y)
text_end = rl.Vector2(description_pos.x + description_size.x - text_margin.x, description_pos.y + description_size.y - text_margin.y)
text_area = rl.Vector2(text_end.x - text_start.x, text_end.y - text_start.y)


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

def equip_item(inventory: dict, item_key: str, player: Player):
    add = True
    item = get_item(item_key)

    for stat, num in item["requirements"].items():
        if player.__getattribute__(stat) < num:
            add = False

    types = {"head": 1, "chest": 1, "legs": 1, "feet": 1,
             "weapons": 1, "necklaces": 1, "bracelets": 2, "rings": 7}


    count = [count for item_key, count in inventory["equips"].items() if get_item(item_key)["type"] == item["type"]]
    if count:
        total = 0
        for num in count:
            total += num
        if total >= types[item["type"]]:
            add = False

    if add:
        edit_inventory(inventory, item_key, 1, equips = True)


def unequip_item(inventory: dict, item: str):
    edit_inventory(inventory, item, -1, equips = True)


def draw_equips(inventory: dict, desc_item: str, mouse: rl.Vector2, textures: dict, equips: dict) -> str:
    remove_name = ""
    rl.draw_texture_ex(textures["equips"], equips_pos, 0, scale, rl.WHITE)

    types = {"weapons": weapon_pos, "head": head_pos, "chest": chest_pos, "legs": legs_pos, "feet": feet_pos,
             "necklaces": necklace_pos, "bracelets": bracelet_pos, "rings": ring_pos}
    for type, value in types.items():
        pos = rl.Vector2(value.x, value.y)
        # item = dict[[(item_key, count) for item_key, count in inventory["equips"].items() if get_item(item_key)["type"] == item["type"]])
        items = dict([(item_key, count) for item_key, count in equips.items() if get_item(item_key)["type"] == type])
        # items = {}
        # for item_key, item_count in equips.items():
        #     item = get_item(item_key)
        #     if item["type"] == type:
                # items[item_key] = item


        for item_key, count in items.items():
            for i in range(count):
                if pos.x <= mouse.x <= pos.x + img_size and pos.y <= mouse.y <= pos.y + img_size:
                    desc_item = item_key
                    rl.draw_texture_ex(textures["highlight"], rl.Vector2(pos.x - scale, pos.y - scale), 0, scale, rl.WHITE)
                    if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT):
                        remove_name = item_key

                rl.draw_texture_ex(textures["blank_equip"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
                rl.draw_texture_ex(textures[item_key], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)

                pos.x += item_margin
                if pos.x == equips_end:
                    pos.x = weapon_pos.x
                    pos.y += item_margin


    if remove_name != "":
        unequip_item(inventory, remove_name)

    return desc_item

def draw_items(font: rl.Font, font_size: float, player: Player, inventory: dict, equipables: bool, desc_item: str, mouse: rl.Vector2,
               textures: dict, items: dict) -> tuple[str, bool]:
    remove_name = ""
    journal = False
    rl.draw_texture_ex(textures["inventory"], inventory_pos, 0, scale, rl.WHITE)


    pos = rl.Vector2(item_pos.x, item_pos.y)
    for item_key, item_count in items.items():
        if pos.x <= mouse.x <= pos.x + img_size and pos.y <= mouse.y <= pos.y + img_size:
            desc_item = item_key
            rl.draw_texture_ex(textures["highlight"], rl.Vector2(pos.x - scale, pos.y - scale), 0, scale, rl.WHITE)
            # if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT) and get_item(item_key)["inventory"] in types.equipables:
            if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT) and equipables:
                remove_name = item_key
            if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT) and item_key == "journal":
                journal = True


        text = str(item_count)
        size = rl.measure_text_ex(font, text, font_size, spacing)

        rl.draw_texture_ex(textures[f"{item_key}"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
        rl.draw_text_ex(font, text, rl.Vector2(pos.x, pos.y + img_size - size.y//2), font_size, spacing, rl.BLACK)

        pos.x += item_margin
        if pos.x > inventory_pos.x + inventory_size.x - inventory_margin * 2:
            pos.x = item_pos.x
            pos.y += item_margin

    if remove_name != "":
        equip_item(inventory, remove_name, player)

    return desc_item, journal



def draw_description(font: rl.Font, font_size: float, text_font_size: float, textures: dict, item_key: str):
    color = rl.BLACK
    rl.draw_texture_ex(textures["description"], description_pos, 0, scale, rl.WHITE)

    if item_key:
        item = get_item(item_key)

        # Draw Item Name
        name_size = rl.measure_text_ex(font, item["name"], font_size, spacing)
        name_pos = rl.Vector2(text_start.x + text_area.x//2, text_start.y)
        u.draw_text(font, item["name"], rl.Vector2(name_pos.x, name_pos.y), font_size, spacing, color, text_area.x, True)
        # lines = u.wrap_lines(font, item["name"], font_size, spacing, int(text_area.x))
        # u.draw_wrapped_text(font, lines, rl.Vector2(name_pos.x, name_pos.y), font_size, spacing, color, True)

        # Draw Description
        text_pos = rl.Vector2(text_start.x + text_area.x//2, name_pos.y + name_size.y * 2)
        line_size, line_pos = u.draw_text(font, item["description"], rl.Vector2(text_pos.x, text_pos.y), text_font_size, spacing, color, text_area.x, True)
        # lines = u.wrap_lines(font, item_data["description"], text_font_size, spacing, int(text_area.x))
        # line_size, line_pos = u.draw_wrapped_text(font, lines, rl.Vector2(text_pos.x, text_pos.y), text_font_size, spacing, color, True)
        y_margin = line_size.y + line_size.y // 4
        pos = rl.Vector2(text_start.x, line_pos.y + y_margin * 1.5)



        if item["inventory"] in types.equipables:
            # Draw Requirements
            for stat, num in item["requirements"].items():
                rl.draw_text_ex(font, f"Requires: {num} {stat}", rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
                pos.y += y_margin

        if item["inventory"] in types.equipables or item["inventory"] == types.consumables:
            # Draw Stats
            for stat, num in item["effects"].items():
                u.draw_text(font, f"{stat} + {num}", rl.Vector2(pos.x, pos.y), text_font_size, spacing, color, text_area.x)
                pos.y += y_margin

        # elif item_type == types.items:
        #     # Draw Uses
        #     for use in item_data["uses"]:
        #         rl.draw_text_ex(font, f"Uses: {use}", rl.Vector2(pos.x, pos.y), text_font_size, spacing, color)
        #         pos.y += y_margin

        if item["inventory"] != types.special:
            # Draw Locations
            for location in item["locations"]:
                u.draw_text(font, f"Locations: {location}", rl.Vector2(pos.x, pos.y), text_font_size, spacing, color, text_area.x)
                pos.y += y_margin


def draw_inv_tabs(mouse: rl.Vector2, textures: dict, tabs: list[str], inv_view: str) -> str:
    view = inv_view
    pos = rl.Vector2(tab_pos.x, tab_pos.y)
    for tab in tabs:
        if inv_view == tab:
            y = - 2 * scale
        else:
            y = 0
        rl.draw_texture_ex(textures[f"tab_{tab}"], rl.Vector2(pos.x, pos.y + y), 0, scale, rl.WHITE)

        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            if pos.x + scale <= mouse.x <= pos.x + scale + tab_size.x and pos.y + scale<= mouse.y <= pos.y + scale + tab_size.y:
                view = tab

        pos.x += tab_margin

    return view

def draw_inventory(font, font_size, player: Player, inventory: dict, gold: int, textures: dict, inv_view: str) -> tuple[str, bool]:
    text_font_size = font_size * .75
    # tabs = {
    #     "weapons": ["weapons"],
    #     "armor": ["armor"],
    #     "accessories": ["necklaces", "bracelets", "rings"],
    #     "items": ["items"],
    #     "consumables": ["consumables"],
    #     "special": ["special"]
    # }
    desc_item = ""
    mouse = rl.get_mouse_position()

    draw_stats(font, text_font_size, player, gold, textures)

    desc_item = draw_equips(inventory, desc_item, mouse, textures, inventory["equips"])

    if inv_view in types.equipables:
        equipables = True
    else:
        equipables = False

    desc_item, journal = draw_items(font, font_size, player, inventory, equipables, desc_item, mouse, textures, inventory[inv_view])

    inv_view = draw_inv_tabs(mouse, textures, views.inventory_tabs, inv_view)

    draw_description(font, font_size, text_font_size, textures, desc_item)

    return inv_view, journal
