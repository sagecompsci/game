import pyray as rl

from utilities import utilities as u
from classes.GameState import GameState
import os
from initialize.load_game import load_game
from information import views
from ui.buttons import back_to_main

from information.ui import (
    scale,
    font_size,
    spacing,
    color,
    text_box_small_size as box_size,
    text_box_small_padding as box_padding
)
margin = scale * 2
box_offset = box_size.y + margin

def load_menu(textures: dict[str, rl.Texture], font: rl.Font, state: GameState) -> GameState:
    mouse = rl.get_mouse_position()
    saves = os.listdir("saves")
    height = 0
    for save in saves:
        height += box_offset
    height -= margin

    pos = rl.Vector2(rl.get_screen_width()//2 - box_size.x/2, rl.get_screen_height()//2 - height//2)

    for save in saves:
        save = save.split(".")[0]
        rl.draw_texture_ex(textures["text_box_small"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
        rl.draw_text_ex(font, save, rl.Vector2(pos.x + box_padding.x, pos.y + box_padding.y), font_size, spacing, color)

        if u.mouse_hovering(pos, mouse, box_size):
            rl.draw_texture_ex(textures["text_box_small_highlight"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
            if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
                state.save = save
                state = load_game(state)
                state.view = views.game

        pos.y += box_offset

    # draw back to main menu
    state.view = back_to_main(textures, font, mouse, state.view)

    return state


