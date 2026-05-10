import pyray as rl
from utilities import utilities as u
from save import save_game
from information import views
from classes.GameState import GameState

from information.ui import (
    scale,
    font_size,
    spacing,
    color,
    text_box_small_size as box_size,
    text_box_small_padding as box_padding
)

height = box_size.y + scale * 2 + box_size.y

def pause_menu(textures: dict[str, rl.Texture], font: rl.Font, state: GameState) -> str:
    view = views.pause_menu
    mouse = rl.get_mouse_position()
    pos = rl.Vector2(rl.get_screen_width()/2 - box_size.x/2, rl.get_screen_height()/2 - height/2)
    # draw resume
    rl.draw_texture_ex(textures["text_box_small"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
    rl.draw_text_ex(font, "resume", rl.Vector2(pos.x + box_padding.x, pos.y + box_padding.y), font_size, spacing, color)
    if u.mouse_hovering(pos, mouse, box_size):
        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            view = views.game
        rl.draw_texture_ex(textures["text_box_small_highlight"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)

    pos.y += box_size.y + scale * 2

    # Draw main
    rl.draw_texture_ex(textures["text_box_small"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
    rl.draw_text_ex(font, "main menu", rl.Vector2(pos.x + box_padding.x, pos.y + box_padding.y), font_size, spacing, color)
    if u.mouse_hovering(pos, mouse, box_size):
        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            view = views.main_menu
            save_game(state.save, state.to_dict())
        rl.draw_texture_ex(textures["text_box_small_highlight"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)


    return view


