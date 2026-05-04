import pyray as rl
import math

from my_dataclasses import GameState, Entity, Tile
import utilities as u
from save import save
import inventory
import movement
import journal




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
    for key, tiles in view["tiles"].items():
        pos = u.str_v2(key)
        for tile in tiles:
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

def draw_player_health(font: rl.Font, textures: dict[str, rl.Texture], health: int, max_health: int):
    scale = 8
    pos = rl.Vector2(5 * scale, 5 * scale)
    health_pos = rl.Vector2(pos.x + 1 * scale, pos.y + 1 * scale)
    health_size = rl.Vector2(64 * scale, 7 * scale)

    #Draw health/damage bar
    if health < max_health:
        rl.draw_texture_ex(textures["player_damage"], (health_pos.x, health_pos.y), 0, scale, rl.WHITE )
        width = 62 * scale
        height = 5 * scale
        percent = health / max_health
        new_width = width * percent
        rl.draw_texture_pro(textures["player_health"], (0, 0, new_width, height),
                            (health_pos.x, health_pos.y, new_width, height), (0, 0), 0, rl.WHITE)

    else:
        rl.draw_texture_ex(textures["player_health"], (health_pos.x, health_pos.y), 0, scale, rl.WHITE)

    # Draw Health Bar Border
    rl.draw_texture_ex(textures["player_health_bar"], (pos.x, pos.y), 0, scale, rl.WHITE)

    # Draw Health numbers
    font_size = scale * 4
    spacing = 1
    color = rl.WHITE
    health_text = f"{math.trunc(health)} / {math.trunc(max_health)}"
    text_size = rl.measure_text_ex(font, health_text, font_size, spacing)
    text_pos = rl.Vector2(pos.x + health_size.x//2 - text_size.x//2, pos.y + health_size.y//2 - (text_size.y//3))
    rl.draw_text_ex(font, health_text, text_pos, font_size, spacing, color)



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
        elif state.menu in ("inventory", "journal"):
            state.menu = ""

    if rl.is_key_pressed(rl.KeyboardKey.KEY_F):
        if state.menu == "":
            state.menu = "journal"
        elif state.menu == "journal":
            state.menu = ""

    elif rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
        if state.menu in ("journal", "inventory"):
            state.menu = ""
        else:
            state.menu = "pause"

    if rl.is_key_pressed(rl.KeyboardKey.KEY_G):
        p.health = p.max_health

    state.time += 1

    if state.time % (5 * 60 * 60) == 0:
        save(state)

    if p.health > p.max_health + p.bonus_health:
        p.health = p.max_health + p.bonus_health


    equip_effects(state)

    if state.menu == "":
        movement.open_chest(state.inventory, state.view, p.pos)
        movement.fight_monster(state.inventory, p, state.view["monsters"], state.view, state.tile_size, state.time,
                               state.kills, state.active_quests, state.completed_quests)


        if state.time - state.last_movement > p.speed * 10:
            state.last_movement = state.time
            state.view, state.location = movement.update_movement(p, state.view, state.buildings, state.levels, state.level, state.location, state.tile_size)
            state.camera.target = rl.Vector2(p.pos.x, p.pos.y)
            # keep track of last time of movement, if greater than 7 then walk





    rl.begin_drawing()
    rl.clear_background(rl.LIGHTGRAY)

    rl.begin_mode_2d(state.camera)

    draw(state.view, state.textures, state.player.pos, state.tile_size, state.scale)



    rl.end_mode_2d()

    draw_player_health(state.font, state.textures, state.player.health + state.player.bonus_health, state.player.max_health + state.player.bonus_health)
    if state.menu == "inventory":
        state.inv_view, is_journal = inventory.draw_inventory(state.font, state.font_size, state.player, state.inventory, state.gold, state.textures, state.inv_view)
        if is_journal:
            state.menu = "journal"

    if state.menu == "journal":
        state.journal_tab_view = journal.draw_journal(state.textures, state.journal_tab_view, state.font, state.kills, state.active_quests, state.completed_quests)

    rl.end_drawing()
