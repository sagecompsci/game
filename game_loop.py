import pyray as rl
import math

from classes.GameState import GameState
from classes.Entity import Entity
import utilities.utilities as u
from utilities.get_data import get_quest, get_npc, get_item
from utilities.inventory_util import edit_inventory, edit_dict
from save import save_game
from ui import inventory_ui as inventory, dialog
from classes.Enum import Status
# from inventory import draw_inventory
# from journal import draw_journal
from information import views
from gameplay import gameplay




def equip_effects(state: GameState):
    p = state.player
    p.bonus_health = 0
    p.bonus_defense = 0
    p.bonus_strength = 0
    p.bonus_attack_speed = 0
    p.bonus_speed = 0

    for item_key, item_count in state.inventory["equips"].items():
        item = get_item(item_key)

        for stat, num in item["effects"].items():
            stat = f"bonus_{stat}"
            state.player.__setattr__(stat, state.player.__getattribute__(stat) + (num * item_count))


def draw(map: dict, textures: dict[str, rl.Texture], player_pos: rl.Vector2, tile_size, scale: int):
    for key, tiles in map["tiles"].items():
        pos = u.str_v2(key)
        for tile in tiles:
            pos = u.rotate(tile_size, rl.Vector2(pos.x, pos.y), tile.rotation)
            rl.draw_texture_ex(textures[tile.name], pos, tile.rotation, scale, rl.WHITE)

    if "chests" in map.keys():
        chests = map["chests"]
        for key in chests.keys():
            rotation = chests[key].rotation
            pos = chests[key].rotate_pos

            rl.draw_texture_ex(textures["chest"], pos, rotation, scale, rl.WHITE)

    if "monsters" in map.keys():
        for key, monster in map["monsters"].items():
            rl.draw_texture_ex(textures[monster.image], u.str_v2(key), 0, scale, rl.WHITE)
            draw_monster_health(tile_size, scale, monster, key)

    if "npcs" in map.keys():
        for key, npc in map["npcs"].items():
            rl.draw_texture_ex(textures[npc.image], u.str_v2(key), 0, scale, rl.WHITE)

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
        if state.view == views.game:
            state.view = views.inventory

        elif state.view == views.inventory:
            state.view = views.game

    if rl.is_key_pressed(rl.KeyboardKey.KEY_F):
        if state.view == views.game:
            state.view = views.journal

        elif state.view == views.journal:
            state.view = views.game

    if rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
        if state.view == views.game:
            state.view = views.pause_menu

    if rl.is_key_pressed(rl.KeyboardKey.KEY_G):
        p.health = p.max_health



    state.time += 1

    if state.time % (5 * 60 * 60) == 0:
        save_game(state.save, state.to_dict())


    if p.health > p.max_health + p.bonus_health:
        p.health = p.max_health + p.bonus_health


    equip_effects(state)

    if state.view == views.game:
        gameplay(state)

    # state.quests["available"], state.quests["active"], state.quests["completed"] = (
    #     quests.update_quests(state.quests["available"], state.quests["active"], state.quests["completed"], state.quests["not_available"]))



    rl.begin_drawing()
    rl.clear_background(rl.LIGHTGRAY)

    rl.begin_mode_2d(state.camera)

    if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT):
        if "npcs" in state.map.keys():
            for key, npc in state.map["npcs"].items():
                # check if player is next to
                if u.is_mouse_on_tile(state.camera, key, state.tile_size):
                    state.view = views.dialog
                    state.npc = key

    draw(state.map, state.textures, state.player.pos, state.tile_size, state.scale)


    rl.end_mode_2d()

    draw_player_health(state.font, state.textures, state.player.health + state.player.bonus_health, state.player.max_health + state.player.bonus_health)
    if state.view == views.inventory:
        state.inventory_view, is_journal = inventory.draw_inventory(state.font, state.font_size, state.player,
                                            state.inventory, state.gold, state.textures, state.inventory_view)
        # if is_journal:
        #     state.menu = views.journal
    #
    # if state.view == "journal":
    #     state.journal_tab_view = draw_journal(state.textures, state.journal_tab_view, state.font, state.kills, state.quests["active"], state.quests["completed"], state.all_quests)
    #     pass

    if state.view == views.dialog:
        npc = state.map["npcs"][state.npc]
        quest = state.quests[npc.quest_code]
        state.view = dialog.draw_dialog(state.view, state.textures, state.font, npc, quest)
        if quest.status == Status.need_reward:
            for reward, count in quest.rewards.items():
                if reward == "gold":
                    edit_dict(state.inventory, "gold", count)
                edit_inventory(state.inventory, reward, count)

    rl.end_drawing()
