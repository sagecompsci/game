import pyray as rl
import math

from my_dataclasses import GameState, Entity, Tile
import utilities as u
from save import save
import inventory
import movement




def equip_effects(state: GameState):
    p = state.player
    p.bonus_health = 0
    p.bonus_defense = 0
    p.bonus_strength = 0
    p.bonus_attack_speed = 0
    p.bonus_speed = 0

    for name, item in state.inventory["equips"].items():
        item_type = item.type.split(" ")[0]
        data = u.get_data(name, item_type)

        for stat, num in data.effects.items():
            stat = f"bonus_{stat}"
            state.player.__setattr__(stat, state.player.__getattribute__(stat) + (num * item.count))


def draw(view: dict, textures: dict[str, rl.Texture], player_pos: rl.Vector2, tile_size, scale: int):
    for key, tile in view["tiles"].items():
        pos = u.str_v2(key)
        pos = u.rotate(tile_size, rl.Vector2(pos.x, pos.y), tile.rotation)
        rl.draw_texture_ex(textures[tile.name], pos, tile.rotation, scale, rl.WHITE)

    chests = view["chests"]
    for key in chests.keys():
        rotation = chests[key].rotation
        pos = chests[key].rotate_pos

        rl.draw_texture_ex(textures["chest"], pos, rotation, scale, rl.WHITE)

    for key, monster in view["monsters"].items():
        rl.draw_texture_ex(textures[monster.image], u.str_v2(key), 0, scale, rl.WHITE)
        draw_monster_health(tile_size, scale, monster, key)

    rl.draw_texture_ex(textures["player"], player_pos, 0, scale, rl.WHITE)

def draw_player_health(state: GameState):
    p = state.player
    width = rl.get_screen_width()//4
    height = rl.get_screen_height()//12
    pos = rl.Vector2(u.x_center_screen(width), rl.get_screen_height() - height - 10)
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

def draw_monster_health(tile_size: int, scale, monster: Entity, key: str):
    width = tile_size
    height = tile_size//scale
    pos = u.str_v2(key)
    rl.draw_rectangle(int(pos.x), int(pos.y), width, height, rl.BLACK)
    health_width = (width//monster.max_health) * monster.health
    rl.draw_rectangle(int(pos.x), int(pos.y), int(health_width), height, rl.RED)

def game_loop(state: GameState):
    p = state.player

    if rl.is_key_pressed(rl.KeyboardKey.KEY_E):
        if state.menu == "":
            state.menu = "inventory"
        elif state.menu == "inventory":
            state.menu = ""

    elif rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
        state.menu = "pause"

    if rl.is_key_pressed(rl.KeyboardKey.KEY_F):
        p.health = p.max_health + p.bonus_health

    state.time += 1

    if state.time % (5 * 60 * 60) == 0:
        save(state)

    if p.health > p.max_health + p.bonus_health:
        p.health = p.max_health + p.bonus_health


    equip_effects(state)

    if state.menu == "":
        movement.open_chest(state.inventory, state.view, p.pos)
        movement.fight_monster(state.inventory, p, state.view["monsters"], state.view, state.tile_size, state.time)

        if state.time - state.last_movement > p.speed * 10:
            state.last_movement = state.time
            state.view, state.location = movement.update_movement(p, state.view, state.buildings, state.levels, state.level, state.location, state.tile_size)
            state.camera.target = rl.Vector2(p.pos.x, p.pos.y)
            # keep track of last time of movement, if greater than 7 then walk

        # print()
        # u.print_v2(p.pos)
        # for direction in state.view["tiles"][u.v2_str(rl.Vector2(p.pos.x, p.pos.y))].directions:
        #     print(direction)





    rl.begin_drawing()
    rl.clear_background(rl.LIGHTGRAY)

    rl.begin_mode_2d(state.camera)

    draw(state.view, state.textures, state.player.pos, state.tile_size, state.scale)



    rl.end_mode_2d()
    draw_player_health(state)
    if state.menu == "inventory":
        state.inv_view = inventory.draw_inventory(state.player, state.inventory, state.gold, state.textures, state.inv_view)

    rl.end_drawing()
