import pyray as rl
from classes.GameState import GameState
from classes.Player import Player
from information import views
from utilities import utilities as u


def init()-> GameState:
    rl.init_window(1800, 900, "Game")
    rl.set_exit_key(0)
    rl.set_target_fps(60)
    state = GameState (
        save = "",
        player = Player(
            pos = rl.Vector2(0, 0),
            image = "player",
            health = 0,
            max_health = 0,
            defense = 0,
            strength = 0,
            attack_speed = 0,
            speed = 0,
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
            "accessories": {},
            "items": {},
            "consumables": {},
            "special": {},
        },
        gold = 0,
        quests = {},
        journal = {},
        level = "",
        location = "",
        map = {},
        levels = {},
        buildings = {},
        tile_size = 8,
        scale = 6,
        map_size = 20,
        textures = {},
        camera = rl.Camera2D(),
        time = 0,
        last_movement = 0,
        view = views.main_menu,
        npc = "",
        inventory_view = "weapons",
        journal_view = "creatures",
        font = rl.load_font_ex("font.ttf", 50, None, 0),
        font_size = 25,
    )

    state.tile_size *= state.scale

    state.textures = u.get_files("images")

    offset_x = (rl.get_screen_width()//2)
    offset_y = (rl.get_screen_height()//2)
    state.camera.offset = rl.Vector2(offset_x, offset_y)
    state.camera.target = rl.Vector2(0, 0)
    state.camera.rotation = 0
    state.camera.zoom = 1

    return state