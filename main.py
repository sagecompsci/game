import os
import pyray as rl
from importlib import reload

from my_dataclasses import GameState, Player
from save import save
import gameplay
import create_menus
import utilities as u
import menu
import inventory
import journal
from quests import quests

def init():
    rl.init_window(1800, 900, "Maze")
    rl.set_exit_key(0)
    rl.set_target_fps(60)
    state = GameState(
        save = "",
        player = Player(
            pos = rl.Vector2(0, 0),
            image = "player",
            health = 50,
            max_health = 100,
            defense = 0,
            strength = 1,
            attack_speed = 1,
            speed = 1,
            last_attack = 0,
            bonus_health = 0,
            bonus_defense = 0,
            bonus_strength = 0,
            bonus_attack_speed = 0,
            bonus_speed = 0
        ),
        inventory = {
            "equips": {},
            "weapons": {},
            "armor": {},
            "necklaces": {},
            "bracelets": {},
            "rings": {},
            "items": {},
            "consumables": {},
            "special": {},
        },
        gold = 0,
        available_quests = {},
        active_quests = quests,
        completed_quests = {},
        kills = {},
        level = "one",
        location = "levels",
        view = {},
        levels = {
            "one": {
                "tiles": {},
                "monsters": {},
                "chests": {},
                "doors": {
                    "pos1": {
                        "tiles": {},
                        "monsters": {},
                        "chests": {},
                    }
                }
            },
            "two": {},
        },
        buildings = {
            "one": {},
            "two": {},
        },
        tile_size = 8,
        scale = 3,
        map_size= 20,
        textures = {},
        camera = rl.Camera2D (),
        time = 0,
        last_movement = 0,
        menu = "main",
        inv_view = "weapons",
        journal_tab_view = "creatures",
        font = rl.get_font_default() ,
        font_size = 25,
    )

    state.tile_size *= state.scale

    state.textures = u.get_files("images")

    offset_x = (rl.get_screen_width()//2)
    offset_y = (rl.get_screen_height()//2)
    state.camera.offset = rl.Vector2(offset_x, offset_y)
    state.camera.target = rl.Vector2(state.player.pos.x, state.player.pos.y)
    state.camera.rotation = 0
    state.camera.zoom = 1

    state.font = rl.load_font_ex("font.ttf", 50, None, 0)

    reload(inventory)
    reload(journal)

    return state

def main():
    state = init()
    inv_test(state)

    main_title, main_buttons = create_menus.create_main_menu()
    load_buttons = create_menus.create_load_menu()
    new_button = create_menus.create_new_menu()
    pause_buttons = create_menus.create_pause_menu()

    while not rl.window_should_close():
        if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
            pass

        if state.menu in ("", "inventory", "journal"):
            gameplay.game_loop(state)
        else:
            menu.menu(state, main_title, main_buttons, load_buttons, new_button, pause_buttons)
    if state.save != "":
        save(state)

def inv_test(state):
    u.add_to_inventory(state.inventory["weapons"], "wood_sword",  "weapons", 10)

    u.add_to_inventory(state.inventory["armor"], "grass_headband",  "armor head", 10)
    u.add_to_inventory(state.inventory["armor"], "grass_sash",  "armor chest", 10)
    u.add_to_inventory(state.inventory["armor"], "grass_skirt",  "armor legs", 10)
    u.add_to_inventory(state.inventory["armor"], "grass_sandals",  "armor feet", 10)

    u.add_to_inventory(state.inventory["bracelets"], "grass_cuff",  "bracelets", 10)
    u.add_to_inventory(state.inventory["rings"], "dandelion_ring",  "rings",10)

    u.add_to_inventory(state.inventory["items"], "dandelion", "items", 10)
    u.add_to_inventory(state.inventory["items"], "grass", "items", 10)
    u.add_to_inventory(state.inventory["items"], "leaf", "items", 10)
    u.add_to_inventory(state.inventory["items"], "mushroom", "items", 10)
    u.add_to_inventory(state.inventory["items"], "wood", "items", 10)

    u.add_to_inventory(state.inventory["consumables"], "apple", "consumables", 10)
    u.add_to_inventory(state.inventory["special"], "map", "special", 10)
    u.add_to_inventory(state.inventory["special"], "journal", "special", 10)


main()
