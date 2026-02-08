import os

import pyray as rl

from generate_maze import create_maze
import menus
from my_dataclasses import GameState, Player, InventoryItem
import utilities as u
from items import item_data
from monsters import monster_data


def init():
    rl.init_window(1800, 900, "Maze")
    rl.set_exit_key(0)
    rl.set_target_fps(60)
    state = GameState(
        save = "",
        player = Player(
            pos = rl.Vector2(0, 0),
            image = "player",
            level = 1,
            xp = 0,
            health = 100,
            max_health = 100,
            defense = 0,
            attack = 2,
            speed = 1,
        ),
        next_to = [],
        inventory = {},
        gold = 0,
        maze = {},
        chests = {},
        monsters = {},
        tile_size= 40,
        maze_size= 20,
        textures = {},
        camera = rl.Camera2D (),
        time = 0,
        menu = "main",
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
        state.gold += state.chests[key]
        state.chests.pop(key)

def attack_monster(state: GameState):
    key = u.v2_str(rl.Vector2(state.player.pos.x, state.player.pos.y))
    if key in state.monsters.keys():
        item = state.monsters[key].drops[0]
        if item in state.inventory.keys():
            state.inventory[item].count += 1
        else:
            state.inventory[item] = InventoryItem(
                count = 1,
                item = item_data[item]
            )

        state.monsters.pop(key)


def update_movement(state: GameState):
    pos = state.player.pos
    direction = ""
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
            state.player.pos = rl.Vector2(pos2.x, pos2.y)
            state.camera.target = rl.Vector2(state.player.pos.x, state.player.pos.y)
            state.next_to = get_adjacent_tiles(state)


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

    rl.draw_texture_ex(state.textures[state.player.image], state.player.pos, 0, scale, rl.WHITE)



def game_loop(state: GameState):
    if rl.is_key_pressed(rl.KeyboardKey.KEY_E):
        if state.menu == "":
            state.menu = "inventory"
        elif state.menu == "inventory":
            state.menu = ""

    elif rl.is_key_pressed(rl.KeyboardKey.KEY_ESCAPE):
        state.menu = "pause"

    state.time += 1

    if state.time % (5 * 60 * 60) == 0:
        u.save(state)

    if state.menu == "":
        open_chest(state)
        attack_monster(state)

        if state.time % 7 == 0:
            update_movement(state)



    rl.begin_drawing()
    rl.clear_background(rl.WHITE)

    rl.begin_mode_2d(state.camera)

    draw(state)


    rl.end_mode_2d()
    if state.menu == "inventory":
        menus.draw_inventory(state.textures, state.inventory, state.gold)
    rl.end_drawing()


def main():
    state = init()

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

    u.save(state)


main()


"""
to-do


monsters
    - standard monsters drop low grade items. 
    - evolved monsters drop high grade items
    
    - item drops
    - xp 
    
level system
    - level xp system one of the following
        - follow fibonacci. level 2 requires 100, 3 required 200, 4 requires 300, 5 requires 500, 6 requires 800
        - times 100. 2 requires 200, 3 requires 300, 4 requires 400
    get stats when you level up
        - can assign stats to whatever you want

stats
    - health
        - some weapons require certain amount of health to use
    - strength
        - 1 strength = 1 attack power
        - some weapons require certain amount of strength to use
    - defense
        - defence negates enemy attack. if you have 2 defence and are attacked with 4 attack, you only take 2 damage
    - speed
        - effects speed of attack
        - maybe??? affects walking speed

fighting
    - when you are adjacent to a monster you will automatically attack, monster will automatically attack you
    - entity attacks with attack power every certain number of seconds. (will also show damage per second)
    - crit attack??
    - if there are multiple enemies can choose which to attack first by clicking on them

inventory 
    - large inventory. gets bigger somehow
    - each spot can hold 999
    - infinite amount of gold
    - equips
        - each slot can only have one
        - attack or defence or speed is added or subtracted to player attack or defence
        - weapon, head, chest, leg, boots
    - feature to compare items
        - right click on item, compare
        - right click on second item, compare
        - in the decription area both items will be shown, stacked on top of each other
        - button to stop comparing
         
    on the left side is equips and player
    in the middle is the inventory
    on top are the tabs for different sections
    on the right is the description of the item you are hovering over
   
    - inventory item
        - image
        - count
         
    - description
        - image
        - name
        - description
        - stats
        - location
        - uses
    
    inventory["Item Name"] = [image, count]
    if hovering then description_item = key
        get json object(key)
    

    


minimap
    - only shows where you have walked
    - basic map
        - given by default. in black and white. only shows general landmarks and not exact
    - fairy map
        - if you meet a fairy npc and talk to her she asks if she can come with you. she draws map of every tile everywhere
            you have been. Fairy has always loved maps and adventure, but is too weak to survive on her own

chalk
    - can draw arrows on stone
mirror
    - can see around corners if you are on the tile next to a corner
compass 
    - shows direction you are facing
    
journal
    - stores information about items and monsters that you have seen
    - if you see a monster, then the picture and name is added to the journal along with location of sighting
    - if you kill a monster, the description, stats, and drops will be added to the journal
    - peaceful creatures are same as monsters
    - if you see a weapon in a shop or put a weapon in your inventory, weapon description, pciture, name, stats are added
    - items are same as weapons, also have location info
    
    - has list of all current quests, all dialog lines for that quest, location of quest given
    - has all npcs that you have talked to. lists name, location, profession, and short description of them (maybe logs all conversation)

there are rune things scattered throughout the map that give you stats or other benefits (increase inventory size

levels
    0. Villages
        - somewhere there is an ocean
        - possible biomes (not all will generate)
            - plains
            - forest
            - jungle 
            - frozen
            - desert
            - swamp
            - mountains
        
    1. Maze
        - certain number of entrances.
            - most have villages around them
        - inside of maze corresponds to the biome on the top
            - all, gargoyles
            - plains
            - forest
            - jungle 
            - frozen, zombies
            - desert
            - swamp, slimes
            - mountains, minotaurs
        - can only see a few tiles in front of you. cannot see past walls
        - maze shifts every certain amount of time. monsters respawn. being in the maze while its shifting is very dangerous
            - when maze shifts the entrances close until morning
        - maze does not take up the whole level
            - there is a hidden area around the outside of the maze that can only be found when the maze is shifting
                - some way to get back into the maze or back up to the surface
    
    2. Floating Islands
        - entrance is giant hole in center of the maze
            - if you have an item that lets you float down, people with wings fly around you and observe you as you fall
            - if you don't have item, death screen, but then it says "just kidding". You wake up in a village
        - floor is blessed and that allows people to have wings. When they become an adult they kill a griffin or
            something and get the wings. The wings only work on this floor.
        - if player gets wings they can fly from island to island or fly back up to the maze. if they don't have
            wings they have to use bridges to get to some islands or pay npc to carry them back to maze
        - bottom of the floor is filled with black smoke. It slowly damages you if you touch it. after certain amount of
            time it makes wings stop working
            
    forest floor (roots of the world tree)
    
    final floor
        - world tree is growing upside down at the tip of the pyramid
        - world tree grants you a wish. cutscenes play based on your choice and your stats gold and karma
            - general 
                - evil karma become a villain, depending on stats and gold you could destroy the world
                - bad karma become the ruler of the underground
                - neutral karma live peacefully with your friends, no one bother you again
                - good karma become king, kingdom is very prosperous
                - Righteous karma become ruler of the continent and lead humanity to an unprecedented era of peace 
                
            - power
                - if strength stat is at max, you become a god
                - if strength stat is really low, something else happens thats funny
                
            - wealth
                - if strength stat is low enough you attract a dragon and are not able to kill it, so it takes your gold
                - if money is above certain amount you build a castle out of solid gold
                - if money = 0, something
                - if money is low, "you no longer have to beg for scraps"
            
            - fame
            - eternal life
            - nothing
            
random
    - karma is accumulated by quests and doing good things, bad things give negative karma
    - in not pixel art version of game, drawings of items or monsters in inventory or journal should be sketches with light coloring
    - note keeping section

https://comicvine.gamespot.com/profile/decept_o/lists/animals-creatures-and-monster-characters-from-folk/56033/?page=2

npcs
    any
        - mermaid
        - satyrs
        - charon is an npc on one of the levels
            - maybe in the floating islands he ferries you down to the next level
    0. Villages
        - centaurs wandering merchants

creatures
    any
        - pegasus
        - hippocampi
        - dragon
        - fairy
        - dryad

other (nature, not meant to fight)
    any
        - charybdis
            - creates whirlpools, meant to be undefeatable
        - phoenix
            - large fire, some other creature summons rain to put it out. When the fire goes out, the still burning
                phoenix streaks across the sky leaving behind a rainbow. the phoenix is very colorful and the flames
monsters
    any
        - sirens
            - drops: scale
            
        - unicorns
            - drops: horn
            
        - vampires
        - golems
        - chupacraba??
        - wyvern
        - cu sith???
        - bunyip??
        - imp
        - Quetzalcoatl 
        - ladon (serpent guarding golden apple)
        
        
    0. Villages
        - werewolves
        
        - will o the wisp
            - swamp area
            - drops: wisp
            
    1. Maze
        - minotaur
            - drops: horn, hair/tail, cow hide, hoof
            
        - gargoyles
            - blend into the walls/floor, don't know they are there until you are right in front of them
            - drops: living stone
            
        - zombies in frozen area
            - ice essence
            
        - slimes in slime area
            - slime core
        
    
    2. Floating Islands
        - griffin
            - drops: talons, beak, feathers
        
        - thunderbird
            - rare monsters
            - creates lighting storms around the area
            - drops: wings that you can equip
        
        - harpies
            - drops: corrupted wings, talons, teeth
"""