import os

import pyray as rl
import math
from importlib import reload

from generate_maze import create_maze
import menus
from my_dataclasses import GameState, Player, InventoryItem, Entity
import utilities as u
from data.armor import armor_data
from data.bracelets import bracelet_data
from data.items import item_data
from data.necklaces import necklace_data
from data.rings import ring_data
from data.weapons import weapon_data
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
        next_to = [],
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
        maze = {},
        chests = {},
        monsters= {},
        village_monsters = {},
        tile_size= 40,
        maze_size= 20,
        textures = {},
        camera = rl.Camera2D (),
        time = 0,
        menu = "main",
        inv_view = "weapons"
    )

    files = os.listdir("images")
    for file in files:
        images = os.listdir(f"images/{file}")
        for image in images:
            name = image.split(".")[0]
            state.textures[name] = rl.load_texture(f"images/{file}/{image}")

    offset_x = (rl.get_screen_width()//2)
    offset_y = (rl.get_screen_height()//2)
    state.camera.offset = rl.Vector2(offset_x, offset_y)
    state.camera.target = rl.Vector2(state.player.pos.x, state.player.pos.y)
    state.camera.rotation = 0
    state.camera.zoom = 1

    reload(inventory)

    return state


def get_adjacent_tiles(state: GameState) -> list:
    tiles = []
    key = u.v2_str(rl.Vector2(state.player.pos.x, state.player.pos.y))
    directions = state.maze[key].directions
    for direction in directions:
        pos = u.pos_from_direction(state.tile_size, direction, rl.Vector2(state.player.pos.x, state.player.pos.y))
        tiles.append(u.v2_str(rl.Vector2(pos.x, pos.y)))
    return tiles


def open_chest(state: GameState):
    key = u.v2_str(rl.Vector2(state.player.pos.x, state.player.pos.y))
    if key in state.chests:
        u.add_to_inventory(state, state.chests[key], "weapons", "weapons", 1)
        state.chests.pop(key)


def attack_player(state: GameState, monster: Entity):
    p = state.player
    if state.time - monster.last_attack >= 60 // monster.attack_speed:
        player_damage = math.trunc(monster.strength) - p.defense + p.bonus_defense
        if player_damage > 0:
            p.health -= math.trunc(monster.strength)
        monster.last_attack = state.time


def attack_monster(state: GameState, monster: Entity):
    p = state.player
    if state.time - p.last_attack >= 60 // p.attack_speed + p.bonus_attack_speed:
        monster_damage = math.trunc(p.strength + p.bonus_strength) - monster.defense
        if monster_damage > 0:
            monster.health -= math.trunc(p.strength + p.bonus_strength)
        p.last_attack = state.time


def fight_monster(state: GameState):
    p = state.player
    for key in state.next_to:
        if key in state.monsters.keys():
            monster = state.monsters[key]
            if monster.attack_speed > p.attack_speed + p.bonus_attack_speed:
                attack_player(state, monster)
                if p.health <= 0:
                    print("you died")
                else:
                    attack_monster(state, monster)
            else:
                attack_monster(state, monster)
                if monster.health > 0:
                    attack_player(state, monster)

            if monster.health <= 0:
                for drop, count in monster.drops.items():
                    u.add_to_inventory(state, drop, "items", "items", count)

                for stat, num in monster.stats.items():
                    p.__setattr__(stat, p.__getattribute__(stat) + float(num))

                state.monsters.pop(key)
                break

def equip_effects(state: GameState):
    p = state.player
    p.bonus_health = 0
    p.bonus_defense = 0
    p.bonus_strength = 0
    p.bonus_attack_speed = 0
    p.bonus_speed = 0

    for name, item in state.inventory["equips"].items():
        item_type = item.type.split(" ")[0]
        data = ""
        if item_type == "armor":
            data = armor_data[name]
        elif item_type == "bracelets":
            data = bracelet_data[name]
        elif item_type == "necklaces":
            data = necklace_data[name]
        elif item_type == "rings":
            data = ring_data[name]
        elif item_type == "weapons":
            data = weapon_data[name]

        for stat, num in data.effects.items():
            stat = f"bonus_{stat}"
            state.player.__setattr__(stat, state.player.__getattribute__(stat) + (num * item.count))


def update_movement(state: GameState):
    direction = ""
    pos = state.player.pos
    if rl.is_key_down(rl.KeyboardKey.KEY_W):
        direction = "north"
    elif rl.is_key_down(rl.KeyboardKey.KEY_S):
        direction = "south"
    elif rl.is_key_down(rl.KeyboardKey.KEY_A):
        direction = "west"
    elif rl.is_key_down(rl.KeyboardKey.KEY_D):
        direction = "east"
    key = u.v2_str(rl.Vector2(pos.x, pos.y))

    if direction in state.maze[key].directions:
        pos2 = u.pos_from_direction(state.tile_size, direction, rl.Vector2(pos.x, pos.y))
        if not u.v2_str(rl.Vector2(pos2.x, pos2.y)) in state.monsters:
            for key in state.next_to:
                if key in state.monsters.keys():
                    if state.monsters[key].speed > 0:
                        monster_pos = (rl.Vector2(state.player.pos.x, state.player.pos.y))
                        new_key = u.v2_str(rl.Vector2(monster_pos.x, monster_pos.y))
                        if not new_key in state.monsters.keys():
                            state.monsters[new_key] = state.monsters[key]
                            state.monsters.pop(key)

            state.player.pos = rl.Vector2(pos2.x, pos2.y)
            state.camera.target = rl.Vector2(state.player.pos.x, state.player.pos.y)
            state.next_to = get_adjacent_tiles(state)


def game_loop(state: GameState):
    if rl.is_key_pressed(rl.KeyboardKey.KEY_E):
        if state.menu == "":
            state.menu = "inventory"
        elif state.menu == "inventory":
            state.menu = ""

    elif rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
        state.menu = "pause"

    if rl.is_key_pressed(rl.KeyboardKey.KEY_F):
        state.player.health = state.player.max_health + state.player.bonus_health

    state.time += 1

    if state.time % (5 * 60 * 60) == 0:
        u.save(state)

    if state.player.health > state.player.max_health + state.player.bonus_health:
        state.player.health = state.player.max_health + state.player.bonus_health

    equip_effects(state)

    if state.menu == "":
        open_chest(state)
        fight_monster(state)

        if state.time % (state.player.speed * 7) == 0:
            update_movement(state)



    rl.begin_drawing()
    rl.clear_background(rl.WHITE)

    rl.begin_mode_2d(state.camera)

    draw(state)


    rl.end_mode_2d()
    draw_player_health(state)
    if state.menu == "inventory":
        inventory.draw_inventory(state, state.textures, state.inventory, state.gold)

    rl.end_drawing()

def draw(state: GameState):
    scale = state.tile_size // 8
    for tile in state.maze.values():
        rl.draw_texture_ex(state.textures[tile.tile], tile.rotate_pos, tile.rotation, scale, rl.WHITE)

    for key in state.chests.keys():
        rotation = state.maze[key].rotation
        pos = state.maze[key].rotate_pos

        rl.draw_texture_ex(state.textures["chest"], pos, rotation, scale, rl.WHITE)

    for key, monster in state.monsters.items():
        draw_monster = False

        if monster.image == "gargoyle":
            directions = state.maze[key].directions
            for direction in directions:
                pos = u.pos_from_direction(state.tile_size, direction, u.str_v2(key))
                if state.player.pos.x == pos.x and state.player.pos.y == pos.y:
                    draw_monster = True
        else:
            draw_monster = True

        if draw_monster:
            rl.draw_texture_ex(state.textures[monster.image], u.str_v2(key), 0, scale, rl.WHITE)
            draw_monster_health(state, monster, key)

    rl.draw_texture_ex(state.textures[state.player.image], state.player.pos, 0, scale, rl.WHITE)

def draw_player_health(state: GameState):
    p = state.player
    width = rl.get_screen_width()//4
    height = rl.get_screen_height()//12
    pos = rl.Vector2(menus.x_center_screen(width), rl.get_screen_height() - height - 10)
    rl.draw_rectangle(int(pos.x), int(pos.y), width, height, rl.BLACK)
    total_health = math.trunc(p.max_health) + math.trunc(p.bonus_health)
    health_width = (width/total_health) * p.health
    rl.draw_rectangle(int(pos.x), int(pos.y), int(health_width), height, rl.RED)

    font = rl.get_font_default()
    text = f"{math.trunc(p.health)} / {math.trunc(p.max_health + math.trunc(p.bonus_health))}"
    font_size = height // 2
    spacing = 1
    text_pos = u.center_text(font, text, font_size, spacing, rl.Vector2(pos.x, pos.y), width, height)
    rl.draw_text_ex(font, text, text_pos, font_size, spacing, rl.BLACK)

def draw_monster_health(state: GameState, monster: Entity, key: str):
    width = state.tile_size
    height = state.tile_size//8
    pos = u.str_v2(key)
    rl.draw_rectangle(int(pos.x), int(pos.y), width, height, rl.BLACK)
    health_width = (width//monster.max_health) * monster.health
    rl.draw_rectangle(int(pos.x), int(pos.y), int(health_width), height, rl.RED)


def get_save_name(name: str):
    key = rl.get_char_pressed()

    while key > 0:
        if (48 <= key <= 57) or (65 <= key <= 90) or (97 <= key <= 122) or key == 32:
            # numbers            #uppercase           #lowercase           #space
            name += chr(key)

        key = rl.get_char_pressed()

    if rl.is_key_down(rl.KeyboardKey.KEY_BACKSPACE):
        name = name[:-1]

    return name


def menu(state: GameState, main_title, main_buttons, load_buttons, new_button, pause_buttons):
    while rl.window_should_close() == False and state.menu != "":
        mouse_pos = rl.Vector2(-1000, -1000)
        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            mouse_pos = rl.get_mouse_position()

        if state.menu == "main":
            for b in main_buttons:
                if b.pos.x <= mouse_pos.x <= b.pos.x + b.width and b.pos.y <= mouse_pos.y <= b.pos.y + b.height:
                    state.menu = b.on_click()

        elif state.menu == "load":
            for b in load_buttons:
                if b.pos.x <= mouse_pos.x <= b.pos.x + b.width and b.pos.y <= mouse_pos.y <= b.pos.y + b.height:
                    state.menu = ""
                    state.save = b.text
                    u.load(b.text, state)
                    state.next_to = get_adjacent_tiles(state)

        elif state.menu == "new":
            state.save = get_save_name(state.save)
            new_button.text = state.save
            if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
                if state.save != "":
                    state.menu = ""

                state.maze, start_pos, state.chests, state.monsters = create_maze(state)
                state.player.pos = rl.Vector2(start_pos.x, start_pos.y)
                state.camera.target = rl.Vector2(state.player.pos.x, state.player.pos.y)
                state.next_to = get_adjacent_tiles(state)

        elif state.menu == "pause":
            for b in pause_buttons:
                if b.pos.x <= mouse_pos.x <= b.pos.x + b.width and b.pos.y <= mouse_pos.y <= b.pos.y + b.height:
                    state.menu = b.on_click()
                    u.save(state)

            if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
                state.menu = ""

        rl.begin_drawing()
        rl.clear_background(rl.WHITE)

        if state.menu == "main":
            menus.draw_main_menu(state.textures, main_title, main_buttons)
        elif state.menu == "load":
            menus.draw_load_menu(state.textures, load_buttons)
        elif state.menu == "new":
            menus.draw_new_menu(state.textures, new_button)
        elif state.menu == "pause":
            menus.draw_pause_menu(state.textures, pause_buttons)

        rl.end_drawing()


def main():
    state = init()
    inv_test(state)

    main_title, main_buttons = menus.create_main_menu()
    load_buttons = menus.create_load_menu()
    new_button = menus.create_new_menu()
    pause_buttons = menus.create_pause_menu()

    while not rl.window_should_close():
        if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
            pass

        if state.menu == "" or state.menu == "inventory":
            game_loop(state)
        else:
            menu(state, main_title, main_buttons, load_buttons, new_button, pause_buttons)
    if state.save != "":
        u.save(state)

def inv_test(state):
    u.add_to_inventory(state, "sword", "weapons", "weapons", 10)
    u.add_to_inventory(state, "dagger", "weapons", "weapons", 10)

    u.add_to_inventory(state, "grass_hat", "armor", "armor head", 10)
    u.add_to_inventory(state, "grass_shirt","armor",  "armor chest", 10)
    u.add_to_inventory(state, "grass_pants", "armor", "armor legs", 10)
    u.add_to_inventory(state, "grass_shoes", "armor", "armor feet", 10)

    u.add_to_inventory(state, "simple_bracelet", "bracelets", "bracelets", 10)
    u.add_to_inventory(state, "sturdy_bracelet", "bracelets", "bracelets", 10)

    u.add_to_inventory(state, "simple_necklace", "necklaces", "necklaces", 10)

    u.add_to_inventory(state, "ring_one", "rings", "rings",10)
    u.add_to_inventory(state, "ring_two", "rings", "rings",10)
    u.add_to_inventory(state, "ring_three", "rings", "rings",10)

main()

