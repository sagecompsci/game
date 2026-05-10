import pyray as rl
from utilities import utilities as u
from information.ui import (
    scale,
    font_size,
    spacing,
    color,
    text_box_small_size as box_size,
    text_box_small_padding as box_padding
)

from information import views

def back_to_main(textures: dict[str, rl.Texture], font: rl.Font, mouse: rl.Vector2, view: str) -> str:
    pos = rl.Vector2(box_size.x // 5, box_size.x // 5)
    rl.draw_texture_ex(textures["text_box_small"], pos, 0, scale, rl.WHITE)
    rl.draw_text_ex(font, views.main_menu, rl.Vector2(pos.x + box_padding.x, pos.y + box_padding.y), font_size, spacing,color)
    if u.mouse_hovering(pos, mouse, box_size):
        rl.draw_texture_ex(textures["text_box_small_highlight"], rl.Vector2(pos.x, pos.y), 0, scale, rl.WHITE)
        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            return views.main_menu

    return view
