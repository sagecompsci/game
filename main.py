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

def init():
    rl.init_window(1800, 900, "Maze")
    rl.set_exit_key(0)
    rl.set_target_fps(60)
    state = GameState(
        save = "",
        player = Player(
            pos = rl.Vector2(0, 0),
            image = "player",
            health = 100,
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
            "items": {}
        },
        gold = 0,
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
        tile_size = 16,
        scale = 3,
        map_size= 20,
        textures = {},
        camera = rl.Camera2D (),
        time = 0,
        last_movement = 0,
        menu = "main",
        inv_view = "weapons"
    )

    state.tile_size *= state.scale

    state.textures = u.get_files("images")

    offset_x = (rl.get_screen_width()//2)
    offset_y = (rl.get_screen_height()//2)
    state.camera.offset = rl.Vector2(offset_x, offset_y)
    state.camera.target = rl.Vector2(state.player.pos.x, state.player.pos.y)
    state.camera.rotation = 0
    state.camera.zoom = 1

    reload(inventory)

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

        if state.menu == "" or state.menu == "inventory":
            gameplay.game_loop(state)
        else:
            menu.menu(state, main_title, main_buttons, load_buttons, new_button, pause_buttons)
    if state.save != "":
        save(state)

def inv_test(state):
    u.add_to_inventory(state.inventory["weapons"], "sword",  "weapons", 10)
    u.add_to_inventory(state.inventory["weapons"], "dagger",  "weapons", 10)

    u.add_to_inventory(state.inventory["armor"], "grass_hat",  "armor head", 10)
    u.add_to_inventory(state.inventory["armor"], "grass_shirt",  "armor chest", 10)
    u.add_to_inventory(state.inventory["armor"], "grass_pants",  "armor legs", 10)
    u.add_to_inventory(state.inventory["armor"], "grass_shoes",  "armor feet", 10)

    u.add_to_inventory(state.inventory["bracelets"], "simple_bracelet",  "bracelets", 10)
    u.add_to_inventory(state.inventory["bracelets"], "sturdy_bracelet",  "bracelets", 10)

    u.add_to_inventory(state.inventory["necklaces"], "simple_necklace",  "necklaces", 10)

    u.add_to_inventory(state.inventory["rings"], "ring_one",  "rings",10)
    u.add_to_inventory(state.inventory["rings"], "ring_two",  "rings",10)
    u.add_to_inventory(state.inventory["rings"], "ring_three",  "rings",10)

main()
