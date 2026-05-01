import pyray as rl
import math

from my_dataclasses import GameState, Entity, Player
import utilities as u



def get_adjacent_tiles(view: dict, player_pos: rl.Vector2, tile_size) -> list:
    tiles = []
    key = u.v2_str(rl.Vector2(player_pos.x, player_pos.y))
    directions = view["tiles"][key].directions
    for direction in directions:
        pos = u.pos_from_direction(tile_size, direction, rl.Vector2(player_pos.x, player_pos.y))
        tiles.append(u.v2_str(rl.Vector2(pos.x, pos.y)))
    return tiles


def open_chest(inventory: dict, view: dict, player_pos: rl.Vector2):
    key = u.v2_str(rl.Vector2(player_pos.x, player_pos.y))
    if key in view["chests"]:
        u.add_to_inventory(inventory["weapons"], view["chests"][key], "weapons", 1)
        view["chests"].pop(key)


def attack_player(player: Player, monster: Entity, time: int):
    if time - monster.last_attack >= 60 // monster.attack_speed:
        player_damage = math.trunc(monster.strength) - player.defense + player.bonus_defense
        if player_damage > 0:
            player.health -= math.trunc(monster.strength)
        monster.last_attack = time


def attack_monster(player: Player, monster: Entity, time: int):
    if time - player.last_attack >= 60 // player.attack_speed + player.bonus_attack_speed:
        monster_damage = math.trunc(player.strength + player.bonus_strength) - monster.defense
        if monster_damage > 0:
            monster.health -= math.trunc(player.strength + player.bonus_strength)
        player.last_attack = time


def fight_monster(inventory: dict, player: Player, monsters: dict, view: dict, tile_size: int, time: int):
    adjacent_tiles = get_adjacent_tiles(view, rl.Vector2(player.pos.x, player.pos.y), tile_size)
    for key in adjacent_tiles:
        if key in monsters.keys():
            monster = monsters[key]
            if monster.attack_speed > player.attack_speed + player.bonus_attack_speed:
                attack_player(player, monster, time)
                if player.health <= 0:
                    print("you died")
                else:
                    attack_monster(player, monster, time)
            else:
                attack_monster(player, monster, time)
                if monster.health > 0:
                    attack_player(player, monster, time)

            if monster.health <= 0:
                for drop, count in monster.drops.items():
                    u.add_to_inventory(inventory["items"], drop,  "items", count)

                for stat, num in monster.stats.items():
                    player.__setattr__(stat, player.__getattribute__(stat) + float(num))

                monsters.pop(key)
                break

def update_movement(player: Player, view: dict, buildings: dict, levels: dict, level: str, location: str, tile_size) -> tuple[dict, str]:
    direction = ""
    if rl.is_key_down(rl.KeyboardKey.KEY_W):
        direction = "north"
    elif rl.is_key_down(rl.KeyboardKey.KEY_S):
        direction = "south"
    elif rl.is_key_down(rl.KeyboardKey.KEY_A):
        direction = "west"
    elif rl.is_key_down(rl.KeyboardKey.KEY_D):
        direction = "east"

    key = u.v2_str(rl.Vector2(player.pos.x, player.pos.y))
    pos2 = u.pos_from_direction(tile_size, direction, rl.Vector2(player.pos.x, player.pos.y))
    key2 = u.v2_str(rl.Vector2(pos2.x, pos2.y))

    if direction in view["tiles"][key].directions:
        monsters = view["monsters"]
        if not key2 in monsters:
            player.pos = rl.Vector2(pos2.x, pos2.y)
            # for key in get_adjacent_tiles(view, rl.Vector2(player.pos.x, player.pos.y), tile_size):
            #     if key in monsters.keys():
            #         if monsters[key].speed > 0:
            #             monster_pos = (rl.Vector2(player.pos.x, player.pos.y))
            #             new_key = u.v2_str(rl.Vector2(monster_pos.x, monster_pos.y))
            #             if not new_key in monsters.keys():
            #                 monsters[new_key] = monsters[key]
            #                 monsters.pop(key)

    elif key2 in buildings[level].keys():
        if location == "levels":
            view = buildings[level][key2]
            location = "buildings"
        elif location == "buildings":
            view = levels[level]
            location = "levels"

        pos3 = u.pos_from_direction(tile_size, direction, rl.Vector2(pos2.x, pos2.y))
        player.pos = rl.Vector2(pos3.x, pos3.y)


    return view, location