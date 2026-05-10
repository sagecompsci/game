import pyray as rl
from information import views
from initialize.new_game import new_game
from classes.GameState import GameState
from ui.buttons import back_to_main
from information.ui import (
    scale,
    font_size,
    spacing,
    color,
    text_box_small_size as box_size,
    text_box_small_padding as box_padding
)


def get_save_name(name: str):
    key = rl.get_char_pressed()

    while key > 0:
        if (48 <= key <= 57) or (65 <= key <= 90) or (97 <= key <= 122) or key == 32:
            # numbers            #uppercase           #lowercase           #space
            name += chr(key)

        key = rl.get_char_pressed()

    if rl.is_key_pressed(rl.KeyboardKey.KEY_BACKSPACE):
        name = name[:-1]

    return name

def new_menu(textures, font: rl.Font, state) -> GameState:
    mouse = rl.get_mouse_position()
    state.save = get_save_name(state.save)
    state.save = state.save.strip()


    if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
        if state.save != "":
            state.view = views.game
            state = new_game(state)

    pos = rl.Vector2(rl.get_screen_width()//2 - box_size.x//2, rl.get_screen_height()//2 - box_size.y//2)
    rl.draw_texture_ex(textures["text_box_small"], pos, 0, scale, rl.WHITE)
    rl.draw_text_ex(font, state.save, rl.Vector2(pos.x + box_padding.x, pos.y + box_padding.y), font_size, spacing, color)

    state.view = back_to_main(textures, font, mouse, state.view)


    return state